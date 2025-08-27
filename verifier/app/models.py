from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Text)
    input_type = Column(String, CheckConstraint("input_type IN ('text','url')"), nullable=False)
    raw_input = Column(Text, nullable=False)
    status = Column(String, CheckConstraint("status IN ('pending','done','error')"), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey("claims.id", ondelete="CASCADE"))
    source = Column(String, nullable=False)
    url = Column(Text)
    title = Column(Text)
    snippet = Column(Text)
    score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Verdict(Base):
    __tablename__ = "verdicts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(UUID(as_uuid=True), ForeignKey("claims.id", ondelete="CASCADE"), unique=True)
    label = Column(String, CheckConstraint("label IN ('support','contradict','insufficient')"), nullable=False)
    confidence = Column(Float, nullable=False)
    explanation = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
