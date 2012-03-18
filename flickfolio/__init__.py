import os

from sqlalchemy import engine_from_config
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid_beaker import set_cache_regions_from_settings

from flickfolio.resources import Root
from flickfolio.models import initialize_sql, Setting

here = os.path.dirname(os.path.abspath(__file__))

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    theme = Setting.fetch_value('theme')

    def find_renderer(template_file, theme=theme):
        return 'flickfolio:templates/%s/%s' % (theme, template_file)

    set_cache_regions_from_settings(settings)
    session_factory = UnencryptedCookieSessionFactoryConfig(Setting.fetch_value('secret'))
    config = Configurator(root_factory=Root,
                          settings=settings,
                          session_factory=session_factory)
    config.add_route('index','/')
    config.add_route('photosets','/photosets')
    config.add_route('photoset','/photoset/{id}')
    config.add_route('photo','/photo/{id}')
    config.add_route('page','/page/{slug}')
    config.add_route('edit_page','/edit_page/{slug}')
    config.add_route('dashboard','/dashboard')
    config.add_view('flickfolio.views.index_view',
                    route_name='index',
                    renderer=find_renderer('index.mako'))
    config.add_view('flickfolio.views.photosets_view',
                    route_name='photosets',
                    renderer='json')
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
    config.add_static_view('static','flickfolio:static/%s' % theme)
    config.scan()

    return config.make_wsgi_app()