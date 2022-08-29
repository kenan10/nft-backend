from fastapi import FastAPI
from .routers import access_lists
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(access_lists.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
