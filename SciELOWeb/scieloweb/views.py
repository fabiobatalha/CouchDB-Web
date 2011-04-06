from pyramid.config import Configurator
from pyramid.response import Response
from pyramid import exceptions
from pyramid.url import route_url
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.i18n import TranslationStringFactory, negotiate_locale_name, get_localizer

_ = TranslationStringFactory('SciELOWeb')

import urllib2
import pdb
import json

from scieloweb import settings_app

def set_language(request):
    if request.POST:
        local_name = negotiate_locale_name(request)
        resp = Response()
        resp.headers = {'Location': request.referrer}
        resp.status = '302'
        resp.set_cookie('language', local_name)
        a =b
        return resp
    else:
        return HTTPInternalServerError()

def my_view(request):
    return {'project':'scieloweb'}
    
def sci_home(request):
    settings = request.registry.settings
    locale_name = negotiate_locale_name(request) 
    localizer = get_localizer(request)
    
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings_app.WS_CONFIG,
            'main': main,
            '_': _ }    

def sci_alphabetic(request):
    settings = request.registry.settings
    locale_name = negotiate_locale_name(request) 
    localizer = get_localizer(request)
    
    query1    = urllib2.urlopen(settings_app.COUCHDB_VIEWS["sci_alphabetic"])
    query2    = urllib2.urlopen(settings_app.COUCHDB_QUERIES["issues_count_all"])
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
    
    return {'settings': settings_app.WS_CONFIG,
            'document': {"rows":docf},
            'others': { "total_current": len(docf['current']),
                        "total_noncurrent": len(docf['noncurrent']),
                        "all": docjson['rows']
                       },
            'main': main}

def sci_serial(request):
    settings = request.registry.settings
    locale_name = negotiate_locale_name(request) 
    localizer = get_localizer(request)    
    pidval = request.matchdict['pid']
    issn_newtitle = ''
    new_title = ''
    
    query1 = urllib2.urlopen(settings_app.COUCHDB_VIEWS["sci_serial"].format(pid=pidval))
    query2 = urllib2.urlopen(settings_app.COUCHDB_QUERIES["journal_pressreleases"].format(pid=pidval,brac="{}"))
    query3 = urllib2.urlopen(settings_app.COUCHDB_QUERIES["journal_lastarticles"].format(pid=pidval,brac="{}"))
    
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
    
    return {'settings': settings_app.WS_CONFIG,
            'document': document,
            'main': main}

def sci_issues(request):
    settings = request.registry.settings
    locale_name = negotiate_locale_name(request) 
    localizer = get_localizer(request)    
    pidval = request.matchdict['pid']
    issues_dict = {}
    issn_newtitle = ''
    new_title = ''
    
    query1 = urllib2.urlopen(settings_app.COUCHDB_VIEWS["sci_serial"].format(pid=pidval))
    query2 = urllib2.urlopen(settings_app.COUCHDB_VIEWS["sci_issues"].format(pid=pidval,brac="{}"))
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
    
    return {'settings': settings_app.WS_CONFIG,
            'document': document,
            'main': main
            }

def sci_issuetoc(request):
    settings = request.registry.settings
    locale_name = negotiate_locale_name(request) 
    localizer = get_localizer(request)    
    pidval = request.matchdict['pid']
    issues_dict = {}
    issn_newtitle = ''
    new_title = ''
    vol = ''
    num = ''
    year = ''
    month = ''
    serial_sections = ''
    title_translated = ''
    article_default_language = locale_name
    
    query1 = urllib2.urlopen(settings_app.COUCHDB_VIEWS["sci_serial"].format(pid=pidval[0:9]))
    query2 = urllib2.urlopen(settings_app.COUCHDB_VIEWS["sci_issuetoc"].format(pid=pidval))
    query3 = urllib2.urlopen(settings_app.COUCHDB_VIEWS["sci_issue"].format(pid=pidval[0:18]))
    serialjson = json.loads(query1.read())
    articlejson = json.loads(query2.read())
    issuejson =  json.loads(query3.read())
    
    # Creating serial dict just with relevant data
    if serialjson['rows'][0]['doc'].has_key('v400'):
        issn_newtitle = serialjson['rows'][0]['doc']['v400'][0]['_']
        
    if serialjson['rows'][0]['doc'].has_key('v710'):
        new_title = serialjson['rows'][0]['doc']['v710'][0]['_']
        
    if issuejson['rows'][0]['doc'].has_key('v49'):
        issue_sections = issuejson['rows'][0]['doc']['v49']
        
        sections_dict = {}
        for section in issue_sections:
            if sections_dict.has_key(section['l']):
                sections_dict[section['l']][section['c']] = section['t']
            else:
                sections_dict[section['l']] = {section['c']:section['t'] }

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
                "month": month,
                "sections": sections_dict['en']
    }
    
    # Creating article dict just with relevant data for issue toc
    articles = {}
    sections = {}
    for rows in articlejson['rows']:
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

        pid = rows['doc']['v880'][0]['_']
        
        if rows['doc'].has_key('v12'):
            titles = rows['doc']['v12']
            
            titles_dict = {}
            for title in titles:
                if titles_dict.has_key(title['l']):
                    titles_dict[title['l']] = title['_']
                else:
                    titles_dict[title['l']] = ''
                    titles_dict[title['l']] = title['_']

            # getting title according to language
            if titles_dict.has_key(locale_name):
                title_translated = titles_dict[locale_name]
            elif titles_dict.has_key(settings.default_locale_name):
                title_translated = titles_dict[settings.default_locale_name]
            else:
                title_translated = article_default_language        
        
        section = ''
        if rows['doc'].has_key('v49'):
            section = rows['doc']['v49'][0]['_']
            
        if not articles.has_key(pid):
            articles[pid] = {}
            
        articles[pid] = { "pid": pid,
                   "title": title_translated,
               "authors": authors_arr,
               "section": section
               }

    articles_dict_arr = []
    sorted_sections_dc = {}
    sorted_sections_ls = []
    for article in sorted(articles.iterkeys()):
       articles_dict_arr.append(articles[article])
       
       ## Sorting Sections according to the article sort.
       sectionkey = str(articles[article]['section'])
       if not sorted_sections_dc.has_key(sectionkey):
            sorted_sections_dc[articles[article]['section']] =''
            sorted_sections_ls.append(articles[article]['section'])



    
    document = {"serial": serial,
                "articles": articles_dict_arr,
                "sections": sorted_sections_ls
                }
    
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings_app.WS_CONFIG,
            'document': document,
            'main': main
            }

def sci_arttext(request):
    settings = request.registry.settings
    locale_name = negotiate_locale_name(request) 
    localizer = get_localizer(request)    
    pidval = request.matchdict['pid']
    issues_dict = {}
    issn_newtitle = ''
    new_title = ''
    vol = ''
    num = ''
    year = ''
    month = ''
    abstract = ''
    article_default_language = locale_name
    abstract_translated = ''
    title_translated = ''
    keyword_translated = ''
    
    query1 = urllib2.urlopen(settings_app.COUCHDB_VIEWS["sci_serial"].format(pid=pidval[1:10]))
    query2 = urllib2.urlopen(settings_app.COUCHDB_VIEWS["sci_article"].format(pid=pidval[0:23]))
    serialjson = json.loads(query1.read())
    articlejson = json.loads(query2.read())
    
    # Creating serial dict just with relevant data
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
                "newtitle": new_title,
                "vol": vol,
                "num": num,
                "year": year,
                "month": month
    }
    
    # Creating article dict just with the relevant data for abstract page
    pid = articlejson['rows'][0]['doc']['v880'][0]['_']
        
    if articlejson['rows'][0]['doc'].has_key('v40'):  #Article Default language
        article_default_language = articlejson['rows'][0]['doc']['v40']
    
    if articlejson['rows'][0]['doc'].has_key('v83'):  #Abstract
        abstracts = articlejson['rows'][0]['doc']['v83']
        
        abstracts_dict = {}
        for abstract in abstracts:
            if abstracts_dict.has_key(abstract['l']):
                abstracts_dict[abstract['l']] = abstract['a']
            else:
                abstracts_dict[abstract['l']] = ''
                abstracts_dict[abstract['l']] = abstract['a']
        
        # getting abstract according to language
        if abstracts_dict.has_key(locale_name):
            abstract_translated = abstracts_dict[locale_name]
        elif abstracts_dict.has_key(settings.default_locale_name):
            abstract_translated = abstracts_dict[settings.default_locale_name]
        else:
            abstract_translated = article_default_language
            
    if articlejson['rows'][0]['doc'].has_key('v85'):  #Keywords
        keywords = articlejson['rows'][0]['doc']['v85']
        
        keywords_dict = {}
        for keyword in keywords:
            if keyword.has_key('l'):
                if keywords_dict.has_key(keyword['l']):
                    keywords_dict[keyword['l']].append(keyword['k'])
                else:
                    keywords_dict[keyword['l']] = []
                    keywords_dict[keyword['l']].append(keyword['k'])
                    
        # getting keywords according to language
        if keywords_dict.has_key(locale_name):
            keyword_translated = keywords_dict[locale_name]
        elif keywords_dict.has_key(settings.default_locale_name):
            keyword_translated = keywords_dict[settings.default_locale_name]
        else:
            keyword_translated = article_default_language

    if articlejson['rows'][0]['doc'].has_key('v10'): #Authors
        authors = articlejson['rows'][0]['doc']['v10']
        authors_dict = []
        name = ''
        surname = ''
        
        for author in authors:
            if author.has_key('n'):
                name = author['n']
                
            if author.has_key('s'):
                surname = author['s']
                
            authors_dict.append({"surname": surname,"name": name })

    if articlejson['rows'][0]['doc'].has_key('v12'):
        titles = articlejson['rows'][0]['doc']['v12']
        
        titles_dict = {}
        for title in titles:
            if titles_dict.has_key(title['l']):
                titles_dict[title['l']] = title['_']
            else:
                titles_dict[title['l']] = ''
                titles_dict[title['l']] = title['_']

        # getting title according to language
        if titles_dict.has_key(locale_name):
            title_translated = titles_dict[locale_name]
        elif titles_dict.has_key(settings.default_locale_name):
            title_translated = titles_dict[settings.default_locale_name]
        else:
            title_translated = article_default_language
            

    
    article = { "pid": pid,
                "abstract": abstract_translated,
                "keywords": keyword_translated,
                "authors": authors_dict,
                "title": title_translated,
                "doi": settings_app.WS_CONFIG['identity']['doi_prefix']+'/'+pid
    }
    
    document = {    "serial": serial,
                    "article": article 
                }
    
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings_app.WS_CONFIG,
            'document': document,
            'main': main
            }

def sci_abstract(request):
    settings = request.registry.settings
    locale_name = negotiate_locale_name(request) 
    localizer = get_localizer(request)    
    pidval = request.matchdict['pid']
    issues_dict = {}
    issn_newtitle = ''
    new_title = ''
    vol = ''
    num = ''
    year = ''
    month = ''
    abstract = ''
    article_default_language = locale_name
    abstract_translated = ''
    title_translated = ''
    keyword_translated = ''
    
    query1 = urllib2.urlopen(settings_app.COUCHDB_VIEWS["sci_serial"].format(pid=pidval[1:10]))
    query2 = urllib2.urlopen(settings_app.COUCHDB_VIEWS["sci_article"].format(pid=pidval[0:23]))
    serialjson = json.loads(query1.read())
    articlejson = json.loads(query2.read())
    
    # Creating serial dict just with relevant data
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
                "newtitle": new_title,
                "vol": vol,
                "num": num,
                "year": year,
                "month": month
    }
    
    # Creating article dict just with the relevant data for abstract page
    pid = articlejson['rows'][0]['doc']['v880'][0]['_']
        
    if articlejson['rows'][0]['doc'].has_key('v40'):  #Article Default language
        article_default_language = articlejson['rows'][0]['doc']['v40']
    
    if articlejson['rows'][0]['doc'].has_key('v83'):  #Abstract
        abstracts = articlejson['rows'][0]['doc']['v83']
        
        abstracts_dict = {}
        for abstract in abstracts:
            if abstracts_dict.has_key(abstract['l']):
                abstracts_dict[abstract['l']] = abstract['a']
            else:
                abstracts_dict[abstract['l']] = ''
                abstracts_dict[abstract['l']] = abstract['a']
        
        # getting abstract according to language
        if abstracts_dict.has_key(locale_name):
            abstract_translated = abstracts_dict[locale_name]
        elif abstracts_dict.has_key(settings.default_locale_name):
            abstract_translated = abstracts_dict[settings.default_locale_name]
        else:
            abstract_translated = article_default_language
            
    if articlejson['rows'][0]['doc'].has_key('v85'):  #Keywords
        keywords = articlejson['rows'][0]['doc']['v85']
        
        keywords_dict = {}
        for keyword in keywords:
            if keyword.has_key('l'):
                if keywords_dict.has_key(keyword['l']):
                    keywords_dict[keyword['l']].append(keyword['k'])
                else:
                    keywords_dict[keyword['l']] = []
                    keywords_dict[keyword['l']].append(keyword['k'])
                    
        # getting keywords according to language
        if keywords_dict.has_key(locale_name):
            keyword_translated = keywords_dict[locale_name]
        elif abstracts_dict.has_key(settings.default_locale_name):
            keyword_translated = keywords_dict[settings.default_locale_name]
        else:
            keyword_translated = article_default_language

    if articlejson['rows'][0]['doc'].has_key('v10'): #Authors
        authors = articlejson['rows'][0]['doc']['v10']
        authors_dict = []
        name = ''
        surname = ''
        
        for author in authors:
            if author.has_key('n'):
                name = author['n']
                
            if author.has_key('s'):
                surname = author['s']
                
            authors_dict.append({"surname": surname,"name": name })

    if articlejson['rows'][0]['doc'].has_key('v12'):
        titles = articlejson['rows'][0]['doc']['v12']
        
        titles_dict = {}
        for title in titles:
            if titles_dict.has_key(title['l']):
                titles_dict[title['l']] = title['_']
            else:
                titles_dict[title['l']] = ''
                titles_dict[title['l']] = title['_']

        # getting title according to language
        if titles_dict.has_key(locale_name):
            title_translated = titles_dict[locale_name]
        elif abstracts_dict.has_key(settings.default_locale_name):
            title_translated = titles_dict[settings.default_locale_name]
        else:
            title_translated = article_default_language
            

    
    article = { "pid": pid,
                "abstract": abstract_translated,
                "keywords": keyword_translated,
                "authors": authors_dict,
                "title": title_translated,
                "doi": settings_app.WS_CONFIG['identity']['doi_prefix']+'/'+pid
    }
    
    document = {    "serial": serial,
                    "article": article 
                }
    
    main = get_renderer('scieloweb:templates/base.pt').implementation()
    
    return {'settings': settings_app.WS_CONFIG,
            'document': document,
            'main': main
            }