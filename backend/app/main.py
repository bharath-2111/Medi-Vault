from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_session,create_tables
from app.routes import (
    auth
)
app = FastAPI(
    title="Medi-Vault"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"]
)

@app.on_event("startup")
def on_starting():
    create_tables()

@app.get("/")
def get_home():
    return {
        "message": "Welcome to the Medi Vault"
    }


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])