from pyramid.config import Configurator
from pyramid.response import Response
from pyramid import exceptions
from pyramid.url import route_url
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer

import urllib2
import pdb
import json

from scieloweb import settings

def my_view(request):
    return {'project':'SciELOWeb'}
    
def sci_home(request):
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings.WS_CONFIG,
            'main': main}    

def sci_alphabetic(request):
    result = urllib2.urlopen(settings.COUCHDB_VIEWS["sci_alphabetic"]);
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings.WS_CONFIG,
            'document': json.loads(result.read()),
            'main': main}

def sci_serial(request):
    result = urllib2.urlopen(settings.COUCHDB_VIEWS["sci_serial"]);
    return Response(result.read())

def sci_issues(request):
    return Response('Issues')

def sci_issuetoc(request):
    return Response('Issue Toc')

def sci_arttext(request):
    return Response('ArtText')

def sci_abstract(request):
    return Response('Abstract')
