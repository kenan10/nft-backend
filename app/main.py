from fastapi import Depends, FastAPI
from .routers import access_lists
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(access_lists.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
