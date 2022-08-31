from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from ..db import crud, schemas
from sqlalchemy.orm import Session
from ..dependencies import get_db


router = APIRouter(prefix="/lists", tags=["lists"])


@router.get(
    "/list_item",
    response_model=schemas.AccessListItem,
)
async def read_list_item_from_list_if_exist(
    address: str, list_name: str, collection_name: str, db: Session = Depends(get_db)
):
    db_list_item = crud.get_access_list_item_by_list_name_collection_name_and_address(
        db, address=address, list_name=list_name, collection_name=collection_name
    )
    try:
        if db_list_item:
            list_item = schemas.AccessListItem.parse_obj(
                {
                    "wallet_address": db_list_item.wallet.address,
                    "list_name": db_list_item.list.name,
                    "collection_name": db_list_item.list.collection.name,
                    "signed_address": db_list_item.signed_address,
                }
            )
            return list_item
        else:
            raise HTTPException(
                status_code=400, detail="address not found in specified list"
            )
    except ValidationError as e:
        return e


@router.get(
    "/list_items",
    response_model=schemas.AccessListItems,
)
async def read_list_items_from_list_if_exist(
    address: str, collection_name: str, db: Session = Depends(get_db)
):
    db_list_items = crud.get_access_list_items_by_address(
        db, address=address
    )
    
    if db_list_items:
        try:
            data = []
            for item in db_list_items:
                print(item.list.collection.name, collection_name)  
                if item.list.collection.name == collection_name:
                    data.append(
                        schemas.AccessListItem.parse_obj(
                            {
                                "wallet_address": item.wallet.address,
                                "list_name": item.list.name,
                                "collection_name": item.list.collection.name,
                                "signed_address": item.signed_address,
                            }
                        )
                    )
            list_items = schemas.AccessListItems.parse_obj(data)
            return list_items
        except ValidationError as e:
            return e
    else:
        return schemas.AccessListItems()
