CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS claims (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id TEXT,
  input_type TEXT CHECK (input_type IN ('text','url')) NOT NULL,
  raw_input TEXT NOT NULL,
  status TEXT CHECK (status IN ('pending','done','error')) DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS evidence (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  claim_id UUID REFERENCES claims(id) ON DELETE CASCADE,
  source TEXT NOT NULL,  -- 'wikipedia' | 'factcheck' | ...
  url TEXT,
  title TEXT,
  snippet TEXT,
  score DOUBLE PRECISION,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS verdicts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  claim_id UUID UNIQUE REFERENCES claims(id) ON DELETE CASCADE,
  label TEXT CHECK (label IN ('support','contradict','insufficient')) NOT NULL,
  confidence DOUBLE PRECISION NOT NULL,
  explanation TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_claims_user_id ON claims(user_id);
CREATE INDEX IF NOT EXISTS idx_claims_status ON claims(status);
CREATE INDEX IF NOT EXISTS idx_evidence_claim_id ON evidence(claim_id);
CREATE INDEX IF NOT EXISTS idx_evidence_source ON evidence(source);
CREATE INDEX IF NOT EXISTS idx_verdicts_claim_id ON verdicts(claim_id);

