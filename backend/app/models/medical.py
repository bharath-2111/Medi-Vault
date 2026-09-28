from sqlmodel import SQLModel, Field,Relationship
from uuid import UUID, uuid4
from datetime import date,datetime,timezone


class Allergy(SQLModel, table=True):
    __tablename__ = "allergies"
    id: UUID = Field(primary_key=True,default_factory=uuid4)
    patient_id : UUID = Field(foreign_key="patient_profiles.id",index=True)
    allergen : str
    reaction :str
    severity : str
    notes : str
    created_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    patient : "Patient" = Relationship(back_populates="allergies")


class Medication(SQLModel, table=True):
    __tablename__ = "medications"
    id: UUID = Field(primary_key=True,default_factory=uuid4)
    patient_id : UUID = Field(foreign_key="patient_profiles.id",index=True)
    name:str
    dosage :str
    frequency :str
    start_date : date
    end_date : date | None = None
    notes :str
    created_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    patient : 'Patient' = Relationship(back_populates="medications")

class MedicalCondition(SQLModel, table=True):
    __tablename__ = "medical_conditions"
    id: UUID = Field(primary_key=True,default_factory=uuid4)
    patient_id : UUID = Field(foreign_key="patient_profiles.id",index=True) 
    condition_name : str
    diagnosed_date : date
    status : str
    notes : str
    created_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    patient : 'Patient' = Relationship(back_populates="conditions")