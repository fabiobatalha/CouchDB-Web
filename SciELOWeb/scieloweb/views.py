from pyramid.config import Configurator
from pyramid.response import Response
from pyramid import exceptions
from pyramid.url import route_url
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer

def my_view(request):
    return {'project':'SciELOWeb'}
    
def sci_home(request):
    return Response('Home')

def sci_alphabetic(request):
    return Response('Alphabetic')

def sci_serial(request):
    return Response('Serial')

def sci_issues(request):
    return Response('Issues')

def sci_issuetoc(request):
    return Response('Issue Toc')

def sci_arttext(request):
    return Response('ArtText')

def sci_abstract(request):
    return Response('Abstract')
