# -*- coding: utf-8 -*- 

import unittest
import transaction

from sqlalchemy import create_engine
from pyramid import testing
from pyramid.testing import DummyRequest
from flickfolio.models import Base, Setting, DBSession

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            user_id = Setting('user_id', u'69299557@N06')
            user_id.save()
            api_key = Setting('api_key', u'ac8a809ec0883c39965836a9eaf9f04d')
            api_key.save()

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_index_view(self):
        from flickfolio.views import index_view
        request = DummyRequest()
        index_view(request)

    def test_photosets_view(self):
        from flickfolio.views import photosets_view
        request = DummyRequest()
        response = photosets_view(request)
        photosets = response['photosets']
        self.assertEqual(len(photosets), 2)
        self.assertEqual(photosets[0]['title'], u'Набор первый (листья)')
        self.assertEqual(photosets[1]['title'], u'Набор второй (облака)')

#    def test_photoset_view(self):
##        from flickfolio.views import photoset_view
##        request = DummyRequest()
##        request.matchdict['id'] = '72157627894998201'
##        response = photoset_view(request)
##        photoset = response['photoset']
##        self.assertEqual(len(photoset), 1)
##        self.assertEqual(photoset.title, u'Набор первый (листья)')
##        self.assertEqual(photoset[0].title, u'Кленовый лист')