
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Text, Enum, Integer
from database import Base
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB


class Workspace(Base):
    __tablename__ = 'workspace'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False, default=uuid.uuid4)
    name = Column(String(length=150), nullable=False)
    credit = Column(Float(), default=0.0, nullable=False)
    created_at = Column(DateTime(), nullable=True, default=datetime.utcnow)
    modified_at = Column(DateTime(), nullable=True, default=datetime.utcnow)