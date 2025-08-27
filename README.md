# Claim-Checker (Misinformation Detector)

A microservices-based system for detecting misinformation by analyzing claims against evidence from Wikipedia and other sources.

## Architecture

- **Gateway**: FastAPI service handling authentication and public REST API
- **Verifier**: Core pipeline for NLP processing, evidence scoring, and verdict generation
- **Evidence**: Service for fetching evidence from Wikipedia and other sources
- **Database**: PostgreSQL for data persistence

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Running the Application

#### Option 1: Quick Start (Recommended)
1. Clone the repository:
```bash
git clone <your-repo-url>
cd claim_checker
```

2. Start all services using the startup script:
   - **Windows**: Double-click `start.bat` or run `start.bat` in Command Prompt
   - **Linux/Mac**: Run `./start.sh` in terminal

#### Option 2: Manual Start
1. Clone the repository:
```bash
git clone <your-repo-url>
cd claim_checker
```

2. Start all services:
```bash
docker compose up --build -d
```

3. Wait for services to start (about 30-60 seconds)

#### Testing the System

1. **Test with the local test script:**
```bash
python test_local.py
```

2. **Test the API manually:**
```bash
# Login to get JWT token
curl -s http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}' | jq -r .access_token > token.txt

# Verify a claim
curl -s http://localhost:8080/claims/verify \
  -H "Authorization: Bearer $(cat token.txt)" \
  -H "Content-Type: application/json" \
  -d '{"input_type":"text","raw_input":"5G causes COVID"}' | jq

# Get claim by ID (replace <uuid> with actual claim ID)
curl -s http://localhost:8080/claims/<uuid> \
  -H "Authorization: Bearer $(cat token.txt)" | jq
```

3. **View API Documentation:**
   - Gateway API: http://localhost:8080/docs
   - Evidence API: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /auth/login` - Get JWT token

### Claims
- `POST /claims/verify` - Verify a claim (requires JWT)
- `GET /claims/{id}` - Get claim details (requires JWT)

## Development

### Project Structure
```
claim_checker/
├── docker-compose.yml
├── db/
│   └── init.sql
├── gateway/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── security/
│   │   └── models/
│   └── Dockerfile
├── verifier/
│   ├── app/
│   │   ├── main.py
│   │   ├── pipeline.py
│   │   ├── nlp.py
│   │   └── wiki_client.py
│   └── Dockerfile
├── evidence/
│   ├── app/
│   │   ├── main.py
│   │   └── wikipedia.py
│   └── Dockerfile
└── tests/
```

### Environment Variables
Create a `.env` file in the root directory:
```
JWT_SECRET=your-secret-key
DATABASE_URL=postgresql+psycopg://app:app@db:5432/claims
VERIFIER_URL=http://verifier:8000
EVIDENCE_URL=http://evidence:8000
```

## Testing

Run tests with:
```bash
docker compose exec gateway pytest
```

## License

MIT

