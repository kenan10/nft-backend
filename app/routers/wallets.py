from fastapi import APIRouter

router = APIRouter(prefix="/lists", tags=["lists"])


@router.get("/list_items")
async def read_list_items(address: str):
    pass
