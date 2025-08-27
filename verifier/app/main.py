from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Literal
from .database import get_db
from .pipeline import VerificationPipeline
from .models import Base
from .database import engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Claim-Checker Verifier",
    description="Core verification service for the Claim-Checker misinformation detection system",
    version="1.0.0"
)


class VerifyRequest(BaseModel):
    input_type: Literal["text", "url"]
    raw_input: str
    user_id: str


@app.get("/")
async def root():
    return {"message": "Claim-Checker Verifier Service"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "verifier"}


@app.post("/verify")
async def verify_claim(request: VerifyRequest, db: Session = Depends(get_db)):
    """
    Verify a claim using the verification pipeline
    """
    try:
        pipeline = VerificationPipeline(db)
        result = await pipeline.run_pipeline(
            input_type=request.input_type,
            raw_input=request.raw_input,
            user_id=request.user_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")


@app.get("/claims/{claim_id}")
async def get_claim(claim_id: str, db: Session = Depends(get_db)):
    """
    Get claim details by ID
    """
    try:
        pipeline = VerificationPipeline(db)
        result = pipeline.get_claim_details(claim_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Claim not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving claim: {str(e)}")
