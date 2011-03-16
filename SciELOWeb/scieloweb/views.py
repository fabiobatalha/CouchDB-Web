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
    query1    = urllib2.urlopen(settings.COUCHDB_VIEWS["sci_alphabetic"])
    query2    = urllib2.urlopen(settings.COUCHDB_QUERIES["issues_count_all"])
    document  = [];
    docjson   = json.loads(query1.read())
    iss_count = json.loads(query2.read())
    issues_total = {}
    # converting couchdb return to a simple dictionary
    
    for rows2 in iss_count['rows']:
        issues_total[rows2['key']] = rows2['value']
        
    
    for rows in docjson['rows']:
        rows2 = []
        doc = {}
        doc['title'] =        rows['doc']['v100'][0]['_']
        doc['issn'] =         rows['doc']['v400'][0]['_']
        doc['issn2'] =        rows['doc']['v935'][0]['_']
        doc['issn2_type'] =   rows['doc']['v35'][0]['_']
        if issues_total['1678-9741']:
            doc['issues_total'] = issues_total[doc['issn']]
        document.append(doc);
    
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings.WS_CONFIG,
            'document': {"rows":document},
            'main': main}

def sci_serial(request):  
    pidval = request.matchdict['pid']
    #lang   = request.matchdict['lang']
    
    result        = urllib2.urlopen(settings.COUCHDB_VIEWS["sci_serial"].format(pid=pidval));
    pressreleases = urllib2.urlopen(settings.COUCHDB_QUERIES["journal_pressrelases"].format(pid=pidval,brac="{}"));
    lastarticles  = urllib2.urlopen(settings.COUCHDB_QUERIES["journal_lastarticles"].format(pid=pidval,brac="{}"));
    
    document = {"doc": json.loads(result.read()),
                "pressreleases": json.loads(pressreleases.read()),
                "lastarticles": json.loads(lastarticles.read())
                }
    
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings.WS_CONFIG,
            'document': document,
            'main': main}

def sci_issues(request):
    return Response('Issues')

def sci_issuetoc(request):
    return Response('Issue Toc')

def sci_arttext(request):
    return Response('ArtText')

def sci_abstract(request):
    return Response('Abstract')
