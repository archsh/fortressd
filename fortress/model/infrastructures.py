# -*- coding: utf-8 -*-
"""Infrastructures model module."""
from sqlalchemy import *
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime, LargeBinary, SmallInteger
from sqlalchemy.orm import relationship, backref

from fortress.model import DeclarativeBase, metadata, DBSession


class DataCenter(DeclarativeBase):
    __tablename__ = 'infra_data_centers'
    # { Columns
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(32), nullable=False)
    network = Column(String(32), nullable=False)
    description = Column(Unicode(256), nullable=True)
    # }


class DataServer(DeclarativeBase):
    __tablename__ = 'infra_data_servers'
    # { Columns
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(32), nullable=False)
    ipaddr = Column(String(24), nullable=False)
    dc_id = Column(Integer,
                   ForeignKey('infra_data_centers.id', onupdate="CASCADE", ondelete="CASCADE"),
                   index=True)
    port = Column(SmallInteger, default=22)
    users = Column(String(256), default="root")  # user list on server separated by ','
    description = Column(Unicode(256), nullable=True)
    # }
    data_center = relationship('DataCenter',
                               uselist=False,
                               backref=backref("servers", cascade='all, delete-orphan'))


__all__ = ['DataCenter', 'DataServer']
