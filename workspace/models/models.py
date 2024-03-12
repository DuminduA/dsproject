from sqlalchemy.types import DateTime, String, UUID, Float
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import uuid
import datetime

class Credit(Base):
    __tablename__ = 'credit'
    id = Column(UUID(), primary_key=True, index=True, unique=True, nullable=False, default=uuid.uuid4)
    amount = Column(Float(), nullable=False)
    created_at = Column(DateTime(), nullable=True, default=datetime.utcnow)
    modified_at = Column(DateTime(), nullable=True, default=datetime.utcnow)
    workspace_id = Column(UUID(), ForeignKey('workspace.id'), nullable=False)
    # workspace = relationship("Workspace", back_populates="credit")


class Workspace(Base):
    __tablename__ = 'workspace'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False, default=uuid.uuid4)
    name = Column(String(length=150), nullable=False)
    created_at = Column(DateTime(), nullable=True, default=datetime.utcnow)
    modified_at = Column(DateTime(), nullable=True, default=datetime.utcnow)
