from fastapi import FastAPI
from .routers import access_lists, blockchain

app = FastAPI()

app.include_router(access_lists.router)
app.include_router(blockchain.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
