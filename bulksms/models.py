
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Text, Enum, Integer
from .database import Base
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Bulksms(Base):
    __tablename__ = 'bulksms'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False, default=uuid.uuid4)
    name = Column(String(length=150), nullable=False)
    status = Column(Enum(length=150), nullable=False)
    message = Column(Text(), nullable=True)
    contact_count = Column(Integer(), default=0)
    workspace_id = Column(UUID(as_uuid=False), nullable=False)
    total_cost = Column(Float(), default=0.0, nullable=False)
    created_at = Column(DateTime(), nullable=True, default=datetime.utcnow)
    modified_at = Column(DateTime(), nullable=True, default=datetime.utcnow)


class BulksmsInfo(Base):
    __tablename__ = 'bulksms_info'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False, default=uuid.uuid4)
    bulksms_id = Column(UUID(), ForeignKey("bulksms.id"),  nullable=False)
    contact_name = Column(String(length=150), nullable=False)
    contact_number = Column(String(length=15), nullable=False)
    sms_status = Column(String(length=15), nullable=False)
    sms_cost = Column(Float(), default=0.0)
    created_at = Column(DateTime(), nullable=True, default=datetime.utcnow)
    modified_at = Column(DateTime(), nullable=True, default=datetime.utcnow)
    