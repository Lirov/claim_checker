from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, claims

app = FastAPI(
    title="Claim-Checker Gateway",
    description="Gateway service for the Claim-Checker misinformation detection system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(claims.router)


@app.get("/")
async def root():
    return {"message": "Claim-Checker Gateway API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "gateway"}
