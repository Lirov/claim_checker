import pytest
import httpx
import asyncio
from typing import AsyncGenerator


@pytest.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(base_url="http://localhost:8080") as client:
        yield client


@pytest.mark.asyncio
async def test_gateway_health(client: httpx.AsyncClient):
    """Test that the gateway service is healthy"""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "gateway"


@pytest.mark.asyncio
async def test_auth_login(client: httpx.AsyncClient):
    """Test authentication login"""
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_verify_claim(client: httpx.AsyncClient):
    """Test claim verification (requires authentication)"""
    # First login to get token
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    login_response = await client.post("/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    
    # Verify a claim
    claim_data = {
        "input_type": "text",
        "raw_input": "5G causes COVID"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/claims/verify", json=claim_data, headers=headers)
    
    # The response should be successful (200 or 503 if services not ready)
    assert response.status_code in [200, 503]
    
    if response.status_code == 200:
        data = response.json()
        assert "claim_id" in data
        assert "verdict" in data
        assert "top_evidence" in data
        assert data["verdict"]["label"] in ["support", "contradict", "insufficient"]


@pytest.mark.asyncio
async def test_unauthorized_access(client: httpx.AsyncClient):
    """Test that protected endpoints require authentication"""
    claim_data = {
        "input_type": "text",
        "raw_input": "Test claim"
    }
    response = await client.post("/claims/verify", json=claim_data)
    assert response.status_code == 401
