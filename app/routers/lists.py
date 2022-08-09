from fastapi import APIRouter

router = APIRouter()


@router.get("list_items", tags=["lists"])
async def read_list_items(address: str):
    pass

# @router.post("list_items", tags=["lists"])
# async def read_list_items(address: str):
#     pass