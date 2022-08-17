from pydantic import BaseModel
from typing import List

def to_camel(string):
    temp = string.split('_')
    res = temp[0] + ''.join(ele.title() for ele in temp[1:])
    return res

class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

"""
Collection
"""


class CollectionBase(BaseModel):
    name: str


class Collection(CollectionBase):
    class Config:
        orm_mode = True


class CollectionCreate(CollectionBase):
    pass


"""
Wallet
"""


class WalletBase(BaseModel):
    address: str


class Wallet(WalletBase):
    class Config:
        orm_mode = True


class WalletCreate(WalletBase):
    pass


"""
Access list type
"""


class AccessListTypeBase(BaseModel):
    name: str


class AccessListType(AccessListTypeBase):
    class Config:
        orm_mode = True


class AccessListTypeCreate(AccessListTypeBase):
    pass


"""
Access list
"""


class AccessListBase(BaseModel):
    name: str
    collection_id: int
    list_type_id: int


class AccessList(AccessListBase):
    signing_pk: str
    members: List[Wallet]

    class Config:
        orm_mode = True


class AccessListCreate(AccessListBase):
    signing_pk: str | None


"""
AccessListItem
"""


class AccessListItemBase(BaseModel):
    wallet_id: int
    list_id: int
    signed_address: str


class AccessListItem(BaseModel):
    wallet_address: str
    list_name: str
    collection_name: str
    signed_address: str

    class Config:
        orm_mode = True


class AccessListItem(CamelModel):
    wallet_address: str
    list_name: str
    collection_name: str
    signed_address: str

    class Config:
        orm_mode = True


class AccessListItems(BaseModel):
    __root__: List[AccessListItem] = []


class AccessListItemCreate(AccessListItemBase):
    pass
