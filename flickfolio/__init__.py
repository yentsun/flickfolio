import os

from sqlalchemy import engine_from_config
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from flickfolio.resources import Root
from flickfolio.models import initialize_sql

here = os.path.dirname(os.path.abspath(__file__))
THEME = 'sample'

def find_renderer(template_file, theme=THEME):
    return 'flickfolio:templates/%s/%s' % (theme, template_file)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    session_factory = UnencryptedCookieSessionFactoryConfig('kpAnaAUYsau6piJ5pv')
    config = Configurator(root_factory=Root, settings=settings, session_factory=session_factory)
    config.add_route('index','/')
    config.add_route('gallery','/gallery')
    config.add_route('photoset','/photoset/{id}')
    config.add_route('photo','/photo/{id}')
    config.add_route('page','/page/{slug}')
    config.add_route('edit_page','/edit_page/{slug}')
    config.add_route('dashboard','/dashboard')
    config.add_view('flickfolio.views.index_view',
                    route_name='index',
                    renderer=find_renderer('index.mako'))
    config.add_view('flickfolio.views.gallery_view',
                    route_name='gallery',
                    renderer=find_renderer('gallery.mako'))
    config.add_view('flickfolio.views.photoset_view',
                    route_name='photoset',
                    renderer=find_renderer('photoset.mako'))
    config.add_view('flickfolio.views.photo_view',
                    route_name='photo',
                    renderer=find_renderer('photo.mako'))
    config.add_view('flickfolio.views.page_view',
                    route_name='page',
                    renderer=find_renderer('page.mako'))
    config.add_view('flickfolio.views.edit_page_view',
                    route_name='edit_page',
                    renderer=find_renderer('edit_page.mako', '_admin'))
    config.add_view('flickfolio.views.dashboard_view',
                    route_name='dashboard',
                    renderer=find_renderer('dashboard.mako', '_admin'))
    config.add_static_view('static','flickfolio:static/%s' % THEME)
    config.scan()

    return config.make_wsgi_app()