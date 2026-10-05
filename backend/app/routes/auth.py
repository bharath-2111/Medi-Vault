from app.main import get_session
from app.models import (
    PatientRegisterForm,
    ProviderRegisterForm,
    LoginForm,
    Patient,
    Provider,
    User
)
from fastapi import Depends,HTTPException,APIRouter
from sqlmodel import Session,select,or_
from pwdlib import PasswordHash
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import jwt
from datetime import datetime,timezone,timedelta

hasher = PasswordHash.recommended()
router = APIRouter()
OAuth = OAuth2PasswordBearer(tokenUrl="login")

SEC_KEY = "6ef6ad860b99ee1a2070df216d754937"
ALGO = "HS256"


def get_token(head : dict[str,str]):
    time_now = datetime.now(timezone.utc) 
    data = head.copy()
    data['iat'] = time_now
    data['exp'] = time_now + timedelta(minutes=30)

    return jwt.encode(data , SEC_KEY, algorithm=ALGO)

def get_current_user(
    token : Annotated[str, Depends(OAuth)],
    session : Annotated[Session ,Depends(get_session)]
):
    try:
        payload = jwt.decode(
            token,
            SEC_KEY,
            algorithms=[ALGO]
        )

        data = payload.get("sub")
        if not data:
            raise HTTPException(
                status_code=401,
                detail="Invalid payload"
            )
        try:
            user_id = UUID(data)
        except (ValueError,TypeError):
            raise HTTPException(
                status_code=401,
                detail="Invalid user id"
            )
        user = session.exec(
            select(User).where(User.id == user_id)
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User Not Found"
            )
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )
        

@router.post("/register/patient")
def register_patient(det : PatientRegisterForm , session : Session = Depends(get_session)):
    is_exist = session.exec(
        select(User).where(User.email == det.email)
    ).first()

    if is_exist:
        raise HTTPException(
            status_code=400,
            detail="User Already Exist"
        )
    try:
        user = User(
            name=det.username,
            email=det.email,
            password_hash=hasher.hash(det.password),
            role="PATIENT"
        )

        session.add(user)
        session.flush()

        patient = Patient(
            user_id=user.id,
            date_of_birth=det.date_of_birth,
            gender=det.gender,
            blood_group=det.blood_group,
            phone_no=det.phone_no,
            address=det.address,
        )

        session.add(patient)
        session.commit()
        session.refresh(patient)

        return {
            "message": "successfully registered",
            "patient_id" : patient.id
        }
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Transaction Error"
        )

@router.post("/register/provider")
def register_provider(det : ProviderRegisterForm , session : Session = Depends(get_session)):
    is_exist = session.exec(
        select(User).where(User.email == det.email)
    ).first()

    if is_exist:
        raise HTTPException(
            status_code=400,
            detail="User Already Exist"
        )
    try:
        user = User(
            name=det.username,
            email=det.email,
            password_hash=hasher.hash(det.password),
            role="PROVIDER"
        )

        session.add(user)
        session.flush()

        provider = Provider(
            user_id=user.id,
            provider_type=det.provider_type,
            license_no=det.license_no,
            organization=det.organization
        )

        session.add(provider)
        session.commit()
        session.refresh(provider)

        return {
            "message": "successfully registered",
            "provider_id" : provider.id
        }
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Transaction Error"
        )

@router.post("/login")
def login(
    det : LoginForm,
    session : Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(or_(User.email == det.username, User.name == det.username))
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )
    if not hasher.verify(det.password, user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Invalid Password"
        )
    token = get_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role
    })

    return {
        "message": "Logined Successfully",
        "token" : token
    }


@router.get("/me")
def get_user_info(
    curr_user : Annotated[User,Depends(get_current_user)]
):
    return curr_user