from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from flickfolio.models import Page, Setting
from flickfolio.photo import Photoset, Photo, set_cridentials

set_cridentials(Setting.fetch_value('api_key'),
                Setting.fetch_value('user_id'))

def index_view(request):
    return {
    }

def gallery_view(request):
    return {
        'gallery': Photoset.fetch_all()
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