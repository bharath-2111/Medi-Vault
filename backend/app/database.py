from sqlmodel import Session,SQLModel,create_engine
from .models import (
    User,
    Patient,
    Provider,
    AccessRequest,
    AuditLog,
    Consent,
    MedicalRecord,
    Medication,
    PatientRegisterForm,
    ProviderRegisterForm,
    LoginForm
)


sql_lite_url = "sqlite:///schema.db"
engine = create_engine(sql_lite_url,connect_args={"check_same_thread": False})


def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as ses:
        yield ses