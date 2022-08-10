from pydantic import BaseModel

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
    members: list[Wallet]

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


class AccessListItemCreate(AccessListItemBase):
    pass
