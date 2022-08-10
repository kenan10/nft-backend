from fastapi import APIRouter, Depends
from ..db import crud, schemas
from sqlalchemy.orm import Session
from ..dependencies import get_db


router = APIRouter(prefix="lists/", tags=["lists"])


@router.get("list_items/",
            response_model=schemas.AccessListItem,
            response_model_exclude=("wallet", "list_id"))
async def read_list_item_if_exist(address: str, list_name: str,
                                  collection_name: str,
                                  db: Session = Depends(get_db)):
    db_list_item = crud.get_access_list_item(db, address=address,
                                             list_name=list_name,
                                             collection_name=collection_name)
    list_item = schemas.AccessListItem.parse_obj(
        {"wallet_address": db_list_item.wallet.address,
         "list_name": db_list_item.list.name,
         "collection_name": db_list_item.list.collection.name,
         "signed_address": db_list_item.signed_address})
    return list_item.json()
