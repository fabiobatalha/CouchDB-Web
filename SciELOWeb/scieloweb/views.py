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
    docjson   = json.loads(query1.read())
    iss_count = json.loads(query2.read())
    issues_total = {}
    document  = [];
    docf = {}
    docf['current'] = []
    docf['noncurrent'] = []    
    docstatus = ''
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
        if doc['issn'] in issues_total:
            doc['issues_total'] = issues_total[doc['issn']]
        else:
            doc['issues_total'] = 0
      
        if rows['doc']['v50'][0]['_'] == "C":
            if rows['doc'].has_key('v51'):
                if rows['doc']['v51'][0].has_key('d'):
                    docf['noncurrent'].append(doc)
                else:
                    docf['current'].append(doc)
    
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings.WS_CONFIG,
            'document': {"rows":docf},
            'others': { "total_current": len(docf['current']),
                        "total_noncurrent": len(docf['noncurrent']),
                       },
            'main': main}

def sci_serial(request):  
    pidval = request.matchdict['pid']
    #lang   = request.matchdict['lang']
    
    result        = urllib2.urlopen(settings.COUCHDB_VIEWS["sci_serial"].format(pid=pidval))
    pressreleases = urllib2.urlopen(settings.COUCHDB_QUERIES["journal_pressrelases"].format(pid=pidval,brac="{}"))
    lastarticles  = urllib2.urlopen(settings.COUCHDB_QUERIES["journal_lastarticles"].format(pid=pidval,brac="{}"))
    
    document = {"doc": json.loads(result.read()),
                "pressreleases": json.loads(pressreleases.read()),
                "lastarticles": json.loads(lastarticles.read())
                }
    
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings.WS_CONFIG,
            'document': document,
            'main': main}

def sci_issues(request):
    pidval = request.matchdict['pid']
    issues_dict = {}
    
    query1 = urllib2.urlopen(settings.COUCHDB_VIEWS["sci_serial"].format(pid=pidval))
    query2 = urllib2.urlopen(settings.COUCHDB_VIEWS["sci_issues"].format(pid=pidval,brac="{}"))
    issues = json.loads(query2.read())
    
    for rows in issues['rows']:
        vol = ''
        num = ''
        pid = ''
        
        if rows["doc"].has_key('v31'):
            vol = rows["doc"]["v31"][0]["_"]
        
        if rows["doc"].has_key('v32'):    
            num = rows["doc"]["v32"][0]["_"]
        
        pid = rows["key"]
        
        issue_data = {}
        issue_data = { "vol": vol,
                       "num": num,
                       "pid": pid
        }
        year = rows["key"][9:13]
        if issues_dict.has_key(year):
            issues_dict[year].append(issue_data)
        else:
            issues_dict[year] = []            
            issues_dict[year].append(issue_data)
        
    issues_dict_arr = []
      
    for issue in sorted(issues_dict.iterkeys(), reverse=True):
        issues_dict_arr.append({'year':issue,'data':issues_dict[issue]})

    document = {"journal": json.loads(query1.read()),
                "issues": issues_dict_arr
                }
    
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings.WS_CONFIG,
            'document': document,
            'main': main
            }

def sci_issuetoc(request):
    return Response('Issue Toc')

def sci_arttext(request):
    return Response('ArtText')

def sci_abstract(request):
    return Response('Abstract')
