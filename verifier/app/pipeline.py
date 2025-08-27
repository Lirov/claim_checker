from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from .models import Claim, Evidence, Verdict
from .nlp import simple_keywords, similarity_score, detect_refutation_terms
from .wiki_client import wiki_client
import uuid


class VerificationPipeline:
    def __init__(self, db: Session):
        self.db = db

    async def run_pipeline(self, input_type: str, raw_input: str, user_id: str) -> Dict[str, Any]:
        """
        Main pipeline for claim verification
        """
        try:
            # Step 1: Create claim record
            claim = Claim(
                user_id=user_id,
                input_type=input_type,
                raw_input=raw_input,
                status="pending"
            )
            self.db.add(claim)
            self.db.commit()
            self.db.refresh(claim)

            # Step 2: Extract keywords
            keywords = simple_keywords(raw_input)
            
            # Step 3: Fetch evidence
            evidence_list = []
            for keyword in keywords[:3]:  # Use top 3 keywords
                evidence = await wiki_client.search_evidence(keyword, limit=3)
                evidence_list.extend(evidence)

            # Step 4: Score evidence
            scored_evidence = []
            for ev in evidence_list:
                score = similarity_score(raw_input, ev.get("snippet", ""))
                ev["score"] = score
                scored_evidence.append(ev)

            # Sort by score and take top 5
            scored_evidence.sort(key=lambda x: x["score"], reverse=True)
            top_evidence = scored_evidence[:5]

            # Step 5: Generate verdict
            verdict_label, confidence, explanation = self._generate_verdict(
                raw_input, top_evidence
            )

            # Step 6: Save evidence
            for ev in top_evidence:
                evidence = Evidence(
                    claim_id=claim.id,
                    source=ev.get("source", "wikipedia"),
                    url=ev.get("url"),
                    title=ev.get("title"),
                    snippet=ev.get("snippet"),
                    score=ev.get("score", 0.0)
                )
                self.db.add(evidence)

            # Step 7: Save verdict
            verdict = Verdict(
                claim_id=claim.id,
                label=verdict_label,
                confidence=confidence,
                explanation=explanation
            )
            self.db.add(verdict)

            # Step 8: Update claim status
            claim.status = "done"
            self.db.commit()

            return {
                "claim_id": str(claim.id),
                "verdict": {
                    "label": verdict_label,
                    "confidence": confidence,
                    "explanation": explanation
                },
                "top_evidence": [
                    {
                        "source": ev.get("source", "wikipedia"),
                        "title": ev.get("title"),
                        "url": ev.get("url"),
                        "snippet": ev.get("snippet"),
                        "score": ev.get("score", 0.0)
                    }
                    for ev in top_evidence
                ]
            }

        except Exception as e:
            # Update claim status to error
            if 'claim' in locals():
                claim.status = "error"
                self.db.commit()
            raise e

    def _generate_verdict(self, claim_text: str, evidence_list: List[Dict[str, Any]]) -> Tuple[str, float, str]:
        """
        Generate verdict based on evidence
        """
        if not evidence_list:
            return "insufficient", 0.0, "No evidence found to verify this claim."

        # Calculate average similarity score
        scores = [ev.get("score", 0.0) for ev in evidence_list]
        avg_score = sum(scores) / len(scores) if scores else 0.0

        # Check for refutation terms in evidence
        has_refutation = False
        for ev in evidence_list:
            if detect_refutation_terms(ev.get("snippet", "")):
                has_refutation = True
                break

        # Determine verdict based on scores and refutation terms
        if avg_score > 0.3:  # Strong match threshold
            if has_refutation:
                return "contradict", min(avg_score + 0.2, 1.0), "Evidence suggests this claim is contradicted by reliable sources."
            else:
                return "support", min(avg_score + 0.1, 1.0), "Evidence supports this claim based on reliable sources."
        else:
            return "insufficient", avg_score, "Insufficient evidence to determine the accuracy of this claim."

    def get_claim_details(self, claim_id: str) -> Dict[str, Any]:
        """
        Get detailed claim information including evidence and verdict
        """
        claim = self.db.query(Claim).filter(Claim.id == claim_id).first()
        if not claim:
            return None

        evidence = self.db.query(Evidence).filter(Evidence.claim_id == claim.id).all()
        verdict = self.db.query(Verdict).filter(Verdict.claim_id == claim.id).first()

        return {
            "claim_id": str(claim.id),
            "input_type": claim.input_type,
            "raw_input": claim.raw_input,
            "status": claim.status,
            "verdict": {
                "label": verdict.label if verdict else None,
                "confidence": verdict.confidence if verdict else None,
                "explanation": verdict.explanation if verdict else None
            },
            "evidence": [
                {
                    "source": ev.source,
                    "title": ev.title,
                    "url": ev.url,
                    "snippet": ev.snippet,
                    "score": ev.score
                }
                for ev in evidence
            ]
        }
