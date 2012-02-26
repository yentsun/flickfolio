# -*- coding: utf-8 -*-

import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from flickfolio.models import (
    DBSession,
    Base,
    Page,
    Setting
    )

def main(argv=sys.argv):
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        index = Page('index', 1, u'Главная', u'Текст о нас')
        about = Page('about', 2, u'О нас', u'Текст о нас')
        contacts = Page('contacts', 5, u'Контакты', u'Текст о контактах')
        partners = Page('partners', 6, u'Партнеры', u'Текст о партнерах')
        projects = Page('projects', 7, u'Дизайн-проект',u'Текст о дизайн-проектах')
        user_id = Setting('user_id', u'')
        api_key = Setting('api_key', u'')
        DBSession.add_all([index, about, contacts, partners, projects, user_id, api_key])

#main()