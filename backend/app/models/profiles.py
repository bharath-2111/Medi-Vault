from sqlmodel import SQLModel,Field,Relationship
from uuid import UUID,uuid4
from sqlalchemy import Column,JSON
from typing import Optional
from datetime import date,datetime,timezone


class Patient(SQLModel, table=True):
    __tablename__ = 'patient_profile'
    id : UUID = Field(
        primary_key=True,
        default_factory=uuid4
    )
    user_id : UUID = Field(
        foreign_key='users.id',
        unique=True,
        index=True
    )
    date_of_birth : date 
    gender : str | None  = Field(
        default=None,
        max_length=20
    )
    blood_group : str | None = Field(
        default=None,
        max_length=5
    )
    phone : str | None = Field(
        default=None,
        max_length=20
    )
    address : str | None = None
    created_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))


    user : "User" = Relationship(back_populates="patient")

    medical_records : Optional["MedicalRecord"] = Relationship(
        back_populates="patient",
        sa_relationship_kwargs={
            "uselist":False,
            "cascade": "all, delete-orphan"
        }
    )
    medications : list['Medication'] = Relationship(
        back_populates="patient",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan"
        }
    )
    access_requests : list["AccessRequest"] = Relationship(
        back_populates="patient"
    )
    audit_logs : list["AuditLog"] = Relationship(
        back_populates="patient"
    )


class Provider(SQLModel, table=True):
    __tablename__ ="provider_profile"

    id : UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    user_id : UUID = Field(
        foreign_key="users.id",
        index=True,
        unique=True
    )

    provider_type : str | None = Field(
        default=None,
        max_length=50
    )

    license_no : str | None = Field(
        default=None,
        max_length=100
    )

    organization : str | None = Field(
        default=None,
        max_length=255
    )

    created_at : datetime = Field(
        default_factory=lambda : datetime.now(timezone.utc)
    )

    user : "User" = Relationship(
        back_populates="provider"
    )

    access_requests : list["AccessRequest"] = Relationship(
        back_populates="provider"
    )

    audit_logs : list["AuditLog"] = Relationship(
        back_populates="provider"
    )
