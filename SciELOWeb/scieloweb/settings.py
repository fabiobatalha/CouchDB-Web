DEBUG = True
DB_SERVER = 'http://teste.webservices.scielo.org/'
DB_NAME = 'scielobr'

COVER_SIZES = {
    # id:(width, height),
    'sz1':(160, 160),
    'sz2':(180, 180),
}

COUCHDB_VIEWS = { "sci_alphabetic": DB_SERVER+DB_NAME+"/_design/couchdb/_view/title_id?include_docs=true",
                  "sci_serial": DB_SERVER+DB_NAME+"/_design/couchdb/_view/title_id?include_docs=true&key=\"{pid}\"",
                  "sci_issues": DB_SERVER+DB_NAME+"/_design/couchdb/_view/issues_id?include_docs=true",
                  "sci_issuetoc": DB_SERVER+DB_NAME+"/_design/couchdb/_view/issues_id/{pid}?include_docs=true",
                  "sci_abstract": DB_SERVER+DB_NAME+"/_design/couchdb/_view/article_id/{pid}?include_docs=true",
                  "sci_arttext": DB_SERVER+DB_NAME+"/_design/couchdb/_view/article_id/{pid}?include_docs=true",
}


# Website Configurations

WS_CONFIG = { "identity" : {"title": "SciELO Brasil",}}