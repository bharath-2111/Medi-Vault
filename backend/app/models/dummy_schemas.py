from pydantic import BaseModel
from datetime import date

class PatientRegisterForm(BaseModel):
    username : str
    email : str
    password : str
    date_of_birth : str
    blood_group : str
    gender : str
    phone_no : str
    address : str

class ProviderRegisterForm(BaseModel):
    username : str
    email : str
    password : str
    provider_type : str 
    license_no : str
    organization : str

class LoginForm(BaseModel):
    username : str
    password : str