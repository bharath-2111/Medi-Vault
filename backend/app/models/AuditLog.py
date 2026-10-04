from sqlmodel import SQLModel,Field,Relationship
from uuid import UUID,uuid4
from datetime import datetime,timezone
from typing import Optional

class AuditLog(SQLModel,table=True):
    __tablename__ = "audit_log"
    id : UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    patient_id : UUID = Field(
        foreign_key="patient_profile.id",
        index=True
    )

    provider_id : UUID | None = Field(
        foreign_key="provider_profile.id",
        index=True,
        default=None
    )

    action : str = Field(
        max_length=100
    )

    resource : str | None= Field(
        default=None,
        max_length=50
    )

    access_type : str | None = Field(
        default=None,
        max_length=20
    )

    reference_id : UUID | None = None

    reason : str | None = None

    ip_address : str | None = Field(
        default=None,
        max_length=45
    )

    created_at : datetime = Field(
        default_factory=lambda : datetime.now(timezone.utc)
    )

    patient : "Patient"= Relationship(
        back_populates="audit_logs"
    )

    provider: Optional["Provider"]=Relationship(
        back_populates="audit_logs"
    )
