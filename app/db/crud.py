from sqlalchemy.orm import Session

from . import models, schemas


def create_collection(db: Session, collection: schemas.CollectionCreate):
    db_collection = models.Collection(**collection.dict())
    db.add(db_collection)
    db.commit()
    return db_collection


def get_collection(db: Session, name: str):
    return db.query(models.Collection).filter(models.Collection.name == name).first()


def create_wallet(db: Session, wallet: schemas.WalletCreate):
    db_wallet = models.Wallet(**wallet.dict())
    db.add(db_wallet)
    db.commit()
    return db_wallet


def get_wallet(db: Session, address: str):
    return db.query(models.Wallet).filter(models.Wallet.address == address).first()


def create_access_list_type(
    db: Session, access_list_type: schemas.AccessListTypeCreate
):
    db_access_list_type = models.AccessListType(**access_list_type.dict())
    db.add(db_access_list_type)
    db.commit()
    return db_access_list_type


def get_access_list_type_by_id(db: Session, id: int):
    list_type = (
        db.query(models.AccessListType).filter(models.AccessListType.id == id).first()
    )
    return list_type


def get_access_list_type_by_name(db: Session, name: str):
    access_list_type = (
        db.query(models.AccessListType)
        .filter(models.AccessListType.name == name)
        .first()
    )
    return access_list_type


def create_access_list(db: Session, access_list: schemas.AccessListCreate):
    db_access_list = models.AccessList(**access_list.dict())
    db.add(db_access_list)
    db.commit()
    return db_access_list


def get_access_list_by_name_and_collection_name(
    db: Session, name: str, collection_name: str
):
    access_list = (
        db.query(models.AccessList)
        .filter(
            models.AccessList.collection.has(name=collection_name),
            models.AccessList.name == name,
        )
        .first()
    )
    return access_list


def create_access_list_item(
    db: Session, access_list_item: schemas.AccessListItemCreate
):
    db_access_list_item = models.AccessListItem(**access_list_item.dict())
    db.add(db_access_list_item)
    db.commit()
    return db_access_list_item


def get_access_list_item(
    db: Session, address: str, list_id: int
) -> models.AccessListItem | None:
    access_list_item = (
        db.query(models.AccessListItem)
        .filter(
            models.AccessListItem.list_id == list_id,
            models.AccessListItem.wallet.has(address=address),
        )
        .first()
    )
    return access_list_item


def get_access_list_item_by_list_name_collection_name_and_address(
    db: Session, address: str, list_name: str, collection_name: str
):
    wallet = (
        db.query(models.Wallet.id).filter(models.Wallet.address == address).subquery()
    )
    collection = (
        db.query(models.Collection.id)
        .filter(models.Collection.name == collection_name)
        .subquery()
    )
    access_list = (
        db.query(models.AccessList.id)
        .filter(
            models.AccessList.collection_id.in_(collection),
            models.AccessList.name == list_name,
        )
        .subquery()
    )
    access_list_item = (
        db.query(models.AccessListItem)
        .filter(
            models.AccessListItem.wallet_id.in_(wallet),
            models.AccessListItem.list_id.in_(access_list),
        )
        .first()
    )
    return access_list_item


def get_access_list_items_by_address(
    db: Session, address: str
):
    wallet = (
        db.query(models.Wallet.id).filter(models.Wallet.address == address).subquery()
    )
    access_list_item = (
        db.query(models.AccessListItem)
        .filter(
            models.AccessListItem.wallet_id.in_(wallet),
        )
        .all()
    )
    return access_list_item
