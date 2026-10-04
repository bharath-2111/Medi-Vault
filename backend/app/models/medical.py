from sqlmodel import SQLModel, Field,Relationship
from uuid import UUID, uuid4
from sqlalchemy import Column,JSON
from datetime import date,datetime,timezone

class Medication(SQLModel, table=True):
    __tablename__ = "medications"
    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4
    )
    patient_id : UUID = Field(
        foreign_key="patient_profile.id",
        index=True
    )
    name:str = Field(max_length=150)
    dosage :str | None = Field(
        default=None,
        max_length=100
    )
    frequency :str | None = Field(
        default=None,
        max_length=100
    )
    start_date : date
    end_date : date | None = None
    notes :str
    created_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    patient : 'Patient' = Relationship(back_populates="medications")

class MedicalRecord(SQLModel,table=True):
    __tablename__ = "medical_records"
    id:UUID = Field(
        primary_key=True,
        default_factory=uuid4
    )

    patient_id : UUID = Field(
        foreign_key="patient_profile.id",
        index=True,
        unique=True
    )

    allergies : list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False)
    )

    condition: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False)
    )

    critical_nodes : str | None = None

    updated_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    patient: "Patient" = Relationship(back_populates="medical_records")

