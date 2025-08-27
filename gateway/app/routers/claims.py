from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
import httpx
import os
from ..models.claims import (
    VerifyClaimRequest, 
    VerifyClaimResponse, 
    ClaimDetailResponse
)
from ..models.auth import TokenData
from ..security.jwt import get_current_user

router = APIRouter(prefix="/claims", tags=["claims"])

VERIFIER_URL = os.getenv("VERIFIER_URL", "http://verifier:8000")


@router.post("/verify", response_model=VerifyClaimResponse)
async def verify_claim(
    claim_data: VerifyClaimRequest,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Verify a claim by sending it to the verifier service
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{VERIFIER_URL}/verify",
                json={
                    "input_type": claim_data.input_type,
                    "raw_input": claim_data.raw_input,
                    "user_id": current_user.email
                }
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Verifier service error: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Verifier service unavailable: {str(e)}"
        )


@router.get("/{claim_id}", response_model=ClaimDetailResponse)
async def get_claim(
    claim_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Get claim details by ID
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{VERIFIER_URL}/claims/{claim_id}")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Claim not found"
            )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Verifier service error: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Verifier service unavailable: {str(e)}"
        )
