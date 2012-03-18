import locale
from pyramid.httpexceptions import HTTPFound
from pyramid.i18n import get_locale_name
from beaker.cache import cache_region

from flickfolio.models import Page, Setting, GooglePlusPost
from flickfolio.photo import Photoset, Photo, set_cridentials

set_cridentials(Setting.fetch_value('api_key'),
                Setting.fetch_value('user_id'))

@cache_region('long_term', 'posts')
def _fetch_posts():
    GooglePlusPost.API_KEY = Setting.fetch_value('google_api_key')
    GooglePlusPost.USER_ID = Setting.fetch_value('google_user_id')
    posts = GooglePlusPost.fetch_all()
    return posts

def index_view(request):
    """List Google+ posts"""
    locale.setlocale(locale.LC_TIME, get_locale_name(request))
    return {'posts': _fetch_posts()}

def photosets_view(request):
    """List photosets in JSON format"""
    return {
        'photosets': Photoset.fetch_all(True)
    }

def photoset_view(request):
    id = request.matchdict['id']
    return {
        'photoset': Photoset(id)
    }

def photo_view(request):
    id = request.matchdict['id']
    return {
        'photo': Photo(id)  
    }

def page_view(request):
    slug = request.matchdict['slug']
    page = Page.fetch(slug)
    if page is None or page.body == '':
        request.override_renderer = 'under_construction.mako'
        return {}
    return {
        'page': page
    }

def edit_page_view(request):
    slug = request.matchdict['slug']
    page = Page.fetch(slug)
    saveUrl = request.route_path('edit_page', slug=slug)
    if 'body' in request.params:
        page.body = request.params['body']
        page.update()
        request.session.flash(u'<div class="ok">Page updated!</div>')
        return HTTPFound(saveUrl)
    return {
        'page': page,
        'save_url': saveUrl,
    }

def dashboard_view(request):
    return {
        'pages': Page.fetchAll(),
        'settings': Setting.fetch_all()
    }

def portfolio_view(request):
    return {}