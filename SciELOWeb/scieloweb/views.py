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
                        "all": docjson['rows']
                       },
            'main': main}

def sci_serial(request):  
    pidval = request.matchdict['pid']
    issn_newtitle = ''
    new_title = ''
    
    query1 = urllib2.urlopen(settings.COUCHDB_VIEWS["sci_serial"].format(pid=pidval))
    query2 = urllib2.urlopen(settings.COUCHDB_QUERIES["journal_pressreleases"].format(pid=pidval,brac="{}"))
    query3 = urllib2.urlopen(settings.COUCHDB_QUERIES["journal_lastarticles"].format(pid=pidval,brac="{}"))
    
    serialjson = json.loads(query1.read());
    pressreleasesjson = json.loads(query2.read());
    lastarticlesjson  = json.loads(query3.read());
    
    if serialjson['rows'][0]['doc'].has_key('v400'):
        issn_newtitle = serialjson['rows'][0]['doc']['v400'][0]['_']
        
    if serialjson['rows'][0]['doc'].has_key('v710'):
        new_title = serialjson['rows'][0]['doc']['v710'][0]['_']

    serial = {  "pid": serialjson['rows'][0]['doc']['v935'][0]['_'],
                "title": serialjson['rows'][0]['doc']['v150'][0]['_'],
                "acron": serialjson['rows'][0]['doc']['v68'][0]['_'],
                "publisher": serialjson['rows'][0]['doc']['v480'][0]['_'],
                "issn_type": serialjson['rows'][0]['doc']['v35'][0]['_'],
                "issn": serialjson['rows'][0]['doc']['v935'][0]['_'],
                "mission": serialjson['rows'][0]['doc']['v901'][0]['_'],
                "address": serialjson['rows'][0]['doc']['v63'],
                "issn_newtitle": issn_newtitle,
                "newtitle": new_title
    }
    
    document = { "serial": serial,
                 "pressreleases": pressreleasesjson,
                 "lastarticles": lastarticlesjson
    }
    
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings.WS_CONFIG,
            'document': document,
            'main': main}

def sci_issues(request):
    pidval = request.matchdict['pid']
    issues_dict = {}
    issn_newtitle = ''
    new_title = ''
    
    query1 = urllib2.urlopen(settings.COUCHDB_VIEWS["sci_serial"].format(pid=pidval))
    query2 = urllib2.urlopen(settings.COUCHDB_VIEWS["sci_issues"].format(pid=pidval,brac="{}"))
    serialjson = json.loads(query1.read());
    issuesjson = json.loads(query2.read())
    
    if serialjson['rows'][0]['doc'].has_key('v400'):
        issn_newtitle = serialjson['rows'][0]['doc']['v400'][0]['_']
        
    if serialjson['rows'][0]['doc'].has_key('v710'):
        new_title = serialjson['rows'][0]['doc']['v710'][0]['_']

    serial = {  "pid": serialjson['rows'][0]['doc']['v935'][0]['_'],
                "title": serialjson['rows'][0]['doc']['v150'][0]['_'],
                "acron": serialjson['rows'][0]['doc']['v68'][0]['_'],
                "publisher": serialjson['rows'][0]['doc']['v480'][0]['_'],
                "issn_type": serialjson['rows'][0]['doc']['v35'][0]['_'],
                "issn": serialjson['rows'][0]['doc']['v935'][0]['_'],
                "mission": serialjson['rows'][0]['doc']['v901'][0]['_'],
                "address": serialjson['rows'][0]['doc']['v63'],
                "issn_newtitle": issn_newtitle,
                "newtitle": new_title
    }    
    
    for rows in issuesjson['rows']:
        vol = ''
        num = ''
        pid = ''
        sup_vol = '' # creating vars just for debug purpose
        sup_num = '' # creating vars just for debug purpose

        if rows["doc"].has_key('v31'):
            vol = rows["doc"]["v31"][0]["_"]
        
        if rows["doc"].has_key('v32'):    
            num = rows["doc"]["v32"][0]["_"]
            
        #testing if exists a supplement and overwrite the vars "vol" and "num"
        if rows["doc"].has_key('v131'):
            num = "suppl."+rows["doc"]["v131"][0]["_"]
            sup_vol = vol # creating vars just for debug purpose
        if rows["doc"].has_key('v132'):
            num = "suppl."+rows["doc"]["v132"][0]["_"]
            sup_num = num # creating vars just for debug purpose
        
        pid = rows["key"]
        
        issue_data = {}

        if not rows["doc"].has_key('v41'): #testing if is not a press release
            if num != 'ahead' and num !='review' and num != 'provisional': # testing if is not ahead neither review
                issue_data = { "vol": vol,
                               "num": num,
                               "pid": pid,
                               "sup_vol": sup_vol,
                               "sup_num": sup_num,
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

    document = {"serial": serial,
                "issues": issues_dict_arr,
                }
    
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings.WS_CONFIG,
            'document': document,
            'main': main
            }

def sci_issuetoc(request):
    pidval = request.matchdict['pid']
    issues_dict = {}
    issn_newtitle = ''
    new_title = ''
    vol = ''
    num = ''
    year = ''
    month = ''
    
    query1 = urllib2.urlopen(settings.COUCHDB_VIEWS["sci_serial"].format(pid=pidval[0:9]))
    query2 = urllib2.urlopen(settings.COUCHDB_VIEWS["sci_issuetoc"].format(pid=pidval))
    serialjson = json.loads(query1.read())
    articlejson = json.loads(query2.read())
    
    # Creating serial dict just with relevant data
    if serialjson['rows'][0]['doc'].has_key('v400'):
        issn_newtitle = serialjson['rows'][0]['doc']['v400'][0]['_']
        
    if serialjson['rows'][0]['doc'].has_key('v710'):
        new_title = serialjson['rows'][0]['doc']['v710'][0]['_']

    if articlejson['rows'][0]['doc'].has_key('v31'):
        vol = articlejson['rows'][0]['doc']['v31'][0]['_']

    if articlejson['rows'][0]['doc'].has_key('v32'):
        num = articlejson['rows'][0]['doc']['v32'][0]['_']

    if articlejson['rows'][0]['doc'].has_key('v131'):
        vol = articlejson['rows'][0]['doc']['v131'][0]['_']

    if articlejson['rows'][0]['doc'].has_key('v132'):
        num = articlejson['rows'][0]['doc']['v132'][0]['_']
        
    if articlejson['rows'][0]['doc'].has_key('v65'):
        year = articlejson['rows'][0]['doc']['v65'][0]['_'][0:4]
        month = articlejson['rows'][0]['doc']['v65'][0]['_'][5:]

    serial = {  "pid": serialjson['rows'][0]['doc']['v935'][0]['_'],
                "title": serialjson['rows'][0]['doc']['v150'][0]['_'],
                "acron": serialjson['rows'][0]['doc']['v68'][0]['_'],
                "publisher": serialjson['rows'][0]['doc']['v480'][0]['_'],
                "issn_type": serialjson['rows'][0]['doc']['v35'][0]['_'],
                "issn": serialjson['rows'][0]['doc']['v935'][0]['_'],
                "mission": serialjson['rows'][0]['doc']['v901'][0]['_'],
                "address": serialjson['rows'][0]['doc']['v63'],
                "issn_newtitle": issn_newtitle,
                "newtitle": new_title,
                "vol": vol,
                "num": num,
                "year": year,
                "month": month
    }
    
    # Creating article dict just with relevant data for issue toc
    articles_dict_arr = []
    for rows in articlejson['rows']:
        article = {}
        authors_arr = []
        
        # Getting Article Authors
        if rows['doc'].has_key('v10'):
            for authors in rows['doc']['v10']:
                name = ''
                surname = ''
                
                if authors.has_key('n'):
                    name = authors['n']
                    
                if authors.has_key('s'):
                    surname = authors['s']
                    
                author = {}
                author = { "surname": surname,
                           "name": name
                    }
                authors_arr.append(author)
                
        article = { "title": rows['doc']['v12'][0]['_'],
                    "pid": rows['doc']['v880'][0]['_'],
                    "authors": authors_arr
                }
        
        articles_dict_arr.append(article)
        
    
    document = {"serial": serial,
                "articles": articles_dict_arr
                }
    
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings.WS_CONFIG,
            'document': document,
            'main': main
            }

def sci_arttext(request):
    return Response('ArtText')

def sci_abstract(request):
    return Response('Abstract')
