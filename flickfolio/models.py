# -*- coding: utf-8 -*-

import datetime
import transaction
import sys
import urllib2
import simplejson
from sqlalchemy import (Column, String, Integer, Unicode, UnicodeText)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class GooglePlusPost():
    """A post from Google+"""

    USER_ID = None
    API_KEY = None

    def __init__(self, title, date, url):
        self.date = self._make_datetime(date)
        self.title = title
        self.url = url

    def date_(self, format):
        return self.date.strftime(format).decode('utf-8')

    def _make_datetime(self, string):
        return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%fZ')

    @classmethod
    def fetch_all(cls):
        req = urllib2.Request('https://www.googleapis.com/plus/v1/people/%s/activities/public?key=%s' % (cls.USER_ID, cls.API_KEY))
        opener = urllib2.build_opener()
        file = opener.open(req)
        response = simplejson.load(file)
        items = []
        for item in response['items']:
            new_item = cls(item['title'], item['updated'], item['url'])
            if 'actor' in item['object']:
                new_item.author = item['object']['actor']
            else:
                new_item.author = item['actor']
            new_item.comments = item['object']['replies']['totalItems']
            new_item.attachments = []
            for attachment in item['object']['attachments']:
                if new_item.title == '' and 'displayName' in attachment:
                    new_item.title = attachment['displayName']
                if 'content' in attachment:
                    new_item.description = attachment['content']
                new_item.attachments.append(attachment)
            items.append(new_item)
        return items

class Page(Base):
    """ The SQLAlchemy declarative model class for a Page object. """
    __tablename__ = 'pages'
    slug = Column(String(100), primary_key=True)
    menuId = Column(Integer, unique=True)
    title = Column(Unicode(255))
    body = Column(UnicodeText)

    def __init__(self, slug, menuId, title, body):
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