from sqlmodel import SQLModel,Field,Relationship
from uuid import UUID,uuid4
from datetime import date,datetime,timezone


class Patient(SQLModel, table=True):
    __tablename__ = 'patient_profiles'
    id : UUID = Field(primary_key=True, default_factory=uuid4)
    user_id : UUID = Field(foreign_key='users.id',unique=True,index=True)
    date_of_birth : date 
    gender : str | None = None
    blood_group : str | None = None
    phone : str | None = None
    address : str | None = None
    created_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    allergies : list['Allergy'] = Relationship(back_populates="patient")
    medications : list['Medication'] = Relationship(back_populates="patient")
    conditions : list['MedicalCondition'] = Relationship(back_populates="patient")
