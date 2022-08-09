from fastapi import Depends, FastAPI
from .routers import list_items

app = FastAPI()


app.include_router(list_items.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
