from sqlmodel import SQLModel,Field,Relationship
from datetime import datetime,timezone
from uuid import UUID,uuid4
from typing import Optional
from sqlalchemy import Column,JSON


class AccessRequest(SQLModel, table=True):
    __tablename__= "access_request"
    id : UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    patient_id : UUID = Field(
        foreign_key="patient_profile.id",
        unique=True,
        index=True
    )
    provider_id : UUID = Field(
        foreign_key="provider_profile.id",
        unique=True,
        index=True
    )
    access_type : str = Field(
        default="NORMAL",
        max_length=10
    )
    reason : str

    status : str = Field(
        default="PENDING",
        max_length=20
    )

    qr_hash : str | None = Field(
        default=None,
        unique=True
    )

    qr_exp_time : datetime | None = None

    created_at : datetime = Field(
        default_factory=lambda : datetime.now(timezone.utc)
    )

    responsed_at : datetime | None = None

    patient : "Patient"= Relationship(
        back_populates="access_requests"
    )
    provider: "Provider" = Relationship(
        back_populates="access_requests"
    )

    consent : Optional["Consent"] = Relationship(
        back_populates="access_request",
        sa_relationship_kwargs={
            "uselist": False,
            "cascade": "all,delete-orphan"
        }
    )


class Consent(SQLModel,table=True):
    __tablename__ = "consents"
    id : UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    access_request_id : UUID = Field(
        foreign_key="access_request.id",
        unique=True,
        index=True
    )

    patient_id : UUID = Field(
        foreign_key="patient_profile.id",
        index=True
    )

    provider_id : UUID = Field(
        foreign_key="provider_profile.id",
        index=True
    )

    status : str = Field(
        default="ACTIVE",
        max_length=20
    )

    permissions : list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON,nullable=False)
    )

    granted_at : datetime = Field(
        default_factory=lambda : datetime.now(timezone.utc)
    )

    exp_at : datetime

    revoked_at : datetime | None = None

    access_request : "AccessRequest" = Relationship(
        back_populates="consent"
    )