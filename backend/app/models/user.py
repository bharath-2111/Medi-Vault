from sqlmodel import SQLModel,Field,Relationship
from uuid import UUID, uuid4
from datetime import datetime,timezone


class User(SQLModel, table=True):
    __tablename__ = "users"
    id:UUID = Field(primary_key=True,default_factory=uuid4)

    name : str 
    email : str = Field(unique=True,index=True)
    password_hash : str = Field(exclude=True)

    role :str = Field(default="user")
    is_active : bool = Field(default=True)

    created_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    updated_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    patient : 'Patient' = Relationship(
        back_populates="user"
    )

    provider : "Provider" = Relationship(
        back_populates="user"
    )