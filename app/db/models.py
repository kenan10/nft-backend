from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative
from datetime import datetime


@as_declarative()
class Base:
    id = Column(BigInteger, primary_key=True)
    dlm = Column(DateTime, onupdate=datetime.utcnow)
    time_created = Column(DateTime, default=datetime.utcnow)
    status = Column(Integer, default=2)


class Collection(Base):
    __tablename__ = "collection"

    name = Column(String(255), nullable=False)
    tokens = relationship("Token", backref="collection")
    lists = relationship("AccessList", backref="collection")


class Wallet(Base):
    __tablename__ = "wallet"

    address = Column(String(255), unique=True, nullable=False)
    tokens = relationship("Token", backref="owner")
    list_items = relationship("AccessListItem", backref="wallet")


class Token(Base):
    __tablename__ = "token"

    nft_id = Column(BigInteger, nullable=False)
    wallet_id = Column(BigInteger, ForeignKey("wallet.id"))
    collection_id = Column(BigInteger, ForeignKey("collection.id"))
    details = relationship("TokenDetail", backref="token")

    __table_args__ = (UniqueConstraint(
        "nft_id", "collection_id", name="unique_token"),)


class TokenDetailType(Base):
    __tablename__ = "token_detail_type"

    name = Column(String(255), unique=True, nullable=False)
    token_details = relationship("TokenDetail", backref="token_detail_type")


class TokenDetail(Base):
    __tablename__ = "token_detail"

    value = Column(String(255), nullable=False)
    token_id = Column(BigInteger, ForeignKey("token.id"))
    token_detail_type_id = Column(
        BigInteger, ForeignKey("token_detail_type.id"))

    __table_args__ = (UniqueConstraint(
        "token_id", "token_detail_type_id", name="unique_detail"),)


class AccessListType(Base):
    __tablename__ = "list_type"

    name = Column(String(255), nullable=False)
    lists = relationship("AccessList", backref="list_type")


class AccessList(Base):
    __tablename__ = "list"

    name = Column(String(255), nullable=False)
    list_type_id = Column(BigInteger, ForeignKey("list_type.id"))
    collection_id = Column(BigInteger, ForeignKey("collection.id"))
    signing_pk = Column(String(255), nullable=False)
    list_items = relationship("AccessListItem", backref="list")


class AccessListItem(Base):
    __tablename__ = "list_item"

    wallet_id = Column(BigInteger, ForeignKey("wallet.id"))
    list_id = Column(BigInteger, ForeignKey("list.id"))
    signed_address = Column(String(255), nullable=False)

    __table_args__ = (UniqueConstraint(
        "wallet_id", "list_id", name="unique_lister"),)
