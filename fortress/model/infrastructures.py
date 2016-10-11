# -*- coding: utf-8 -*-
"""Infrastructures model module."""
from sqlalchemy import *
from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Integer, Unicode, SmallInteger

from fortress.model import DeclarativeBase


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
    main_ipaddr = Column(String(24), nullable=False)  # Main IP Address
    ext_ipaddrs = Column(String(256), nullable=True)  # External IP Addresses separated by ','.
    dc_id = Column(Integer,
                   ForeignKey('infra_data_centers.id', onupdate="CASCADE", ondelete="CASCADE"),
                   index=True)
    ssh_port = Column(SmallInteger, default=22)
    mapped_port = Column(SmallInteger, default=0)
    default_user = Column(String(32), default="root")
    description = Column(Unicode(256), nullable=True)
    # }
    center = relationship('DataCenter',
                          uselist=False,
                          backref=backref("servers", cascade='all, delete-orphan'))


class ServerUser(DeclarativeBase):
    __tablename__ = 'infra_data_server_users'
    # { Columns
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    server_id = Column(Integer, ForeignKey('infra_data_servers.id', onupdate="CASCADE", ondelete="CASCADE"), index=True)
    # }
    server = relationship('DataServer',
                          uselist=False,
                          backref=backref("users", cascade='all, delete-orphan'))


__all__ = ['DataCenter', 'DataServer', 'ServerUser']
