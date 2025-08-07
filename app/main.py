from fastapi import FastAPI
from app.api.v1 import stego

app = FastAPI(title="Steganography API")

app.include_router(stego.router, prefix="/api/v1/stego", tags=['steganography'])