from pydantic import BaseModel
from typing import List, Literal, Optional
from uuid import UUID


class VerifyClaimRequest(BaseModel):
    input_type: Literal["text", "url"]
    raw_input: str


class EvidenceItem(BaseModel):
    source: str
    title: str
    url: Optional[str] = None
    snippet: str
    score: float


class Verdict(BaseModel):
    label: Literal["support", "contradict", "insufficient"]
    confidence: float
    explanation: str


class VerifyClaimResponse(BaseModel):
    claim_id: UUID
    verdict: Verdict
    top_evidence: List[EvidenceItem]


class ClaimDetailResponse(BaseModel):
    claim_id: UUID
    input_type: str
    raw_input: str
    status: str
    verdict: Verdict
    evidence: List[EvidenceItem]
