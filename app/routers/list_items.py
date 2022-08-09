from fastapi import APIRouter, Depends
from ..db import crud, schemas
from ..db.database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("list_items", tags=["lists"],
            response_model=schemas.AccessListItem,
            response_model_exclude=("wallet", "list_id"))
async def read_list_item_if_exist(address: str, list_name: str,
                                  collection_name: str,
                                  db: Session = Depends(get_db)):
    list_items = crud.get_access_list_item(db, address=address,
                                           list_name=list_name,
                                           collection_name=collection_name)
    return list_items
