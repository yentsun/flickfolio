# -*- coding: utf-8 -*- 

import transaction
import sys
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Page(Base):
    """ The SQLAlchemy declarative model class for a Page object. """
    __tablename__ = 'pages'
    slug = Column(String(100), primary_key=True)
    menuId = Column(Integer, unique=True)
    title = Column(Unicode(255))
    body = Column(UnicodeText)

    def __init__(self,slug, menuId, title, body):
        self.slug = slug
        self.menuId = menuId
        self.title = title
        self.body = body

    @classmethod
    def fetch(cls,slug):
        return DBSession.query(cls).filter_by(slug=slug).first()

    @classmethod
    def fetchAll(cls):
        return DBSession.query(cls)

    def update(self):
        DBSession.add(self)

class Setting(Base):
    """Basic config settings persisted in database"""
    __tablename__ = 'settings'
    name = Column(String(100), primary_key=True)
    value = Column(Unicode(255))

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def save(self):
        DBSession.add(self)

    @classmethod
    def fetch_value(cls, name):
        return DBSession.query(cls).get(name).value

    @classmethod
    def fetch_all(cls):
        return DBSession.query(cls).all()

def populate(session):
    with transaction.manager:
        index = Page('index', 1, u'Home', u'Homepage body')
        about = Page('about', 2, u'About', u'About us body')
        user_id = Setting('user_id', u'')
        api_key = Setting('api_key', u'')
        theme = Setting('theme', u'sample')
        session.add_all([index, about, user_id, api_key, theme])

def initialize_sql(engine, out=sys.stdout):
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate(DBSession)
    except IntegrityError:
        out.write('Database already populated!')
        transaction.abort()