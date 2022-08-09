from fastapi import Depends, FastAPI
from .routers import lists, wallets

app = FastAPI()


app.include_router(lists.router)
app.include_router(wallets.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
