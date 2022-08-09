from sqlalchemy.orm import Session

from . import models, schemas


def create_collection(db: Session, collection: schemas.CollectionCreate):
    db_collection = models.Collection(**collection.dict())
    db.add(db_collection)
    db.commit()
    return db_collection


def get_collection(db: Session, name: str):
    return db.query(models.Collection).filter(models.Collection.name
                                              == name).first()


def create_wallet(db: Session, wallet: schemas.WalletCreate):
    db_wallet = models.Wallet(**wallet.dict())
    db.add(db_wallet)
    db.commit()
    return db_wallet


def get_wallet(db: Session, address: str):
    return db.query(models.Wallet).filter(models.Wallet.address
                                          == address).first()


def create_access_list_type(db: Session,
                            access_list_type: schemas.AccessListTypeCreate):
    db_access_list_type = models.AccessListType(**access_list_type.dict())
    db.add(db_access_list_type)
    db.commit()
    return db_access_list_type


def get_access_list_type_by_id(db: Session, id: int):
    list_type = db.query(models.AccessListType).filter(
        models.AccessListType.id == id).first()
    return list_type


def get_access_list_type_by_name(db: Session, name: str):
    access_list_type = db.query(models.AccessListType).filter(
        models.AccessListType.name == name).first()
    return access_list_type


def create_access_list(db: Session, access_list: schemas.AccessListCreate):
    db_access_list = models.AccessListType(**access_list.dict())
    db.add(db_access_list)
    db.commit()
    return db_access_list


def get_access_list_by_name_and_collection_name(db: Session, name: str,
                                              collection_id: int):
    access_list = db.query(models.AccessList).filter(
        models.AccessList.collection_id == collection_id,
        models.AccessList.name == name).first()
    return access_list


def create_access_list_item(db: Session,
                            access_list_item: schemas.AccessListItemCreate):
    db_access_list_item = models.AccessListType(**access_list_item.dict())
    db.add(db_access_list_item)
    db.commit()
    return db_access_list_item


def get_access_list_item(db: Session, address: str, list_id: int):
    access_list_item = db.query(models.AccessListItem).filter(
        models.AccessListItem.list_id == list_id,
        models.AccessListItem.wallet.has(address=address) 
    ).first()
    return access_list_item