from fastapi import APIRouter, HTTPException, status
from ..models.auth import LoginRequest, LoginResponse
from ..security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """
    Login endpoint - accepts any non-empty credentials for MVP
    In production, this should validate against a user database
    """
    if not login_data.email or not login_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )
    
    # MVP: Accept any non-empty credentials
    # In production, validate against user database
    access_token = create_access_token(data={"sub": login_data.email})
    
    return LoginResponse(access_token=access_token)
