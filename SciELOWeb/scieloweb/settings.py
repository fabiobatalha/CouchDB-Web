DEBUG     = True
DB_SERVER = 'http://teste.webservices.scielo.org/'
DB_NAME   = 'scielobr2'
LIMIT     = 10

COVER_SIZES = {
    # id:(width, height),
    'sz1':(160, 160),
    'sz2':(180, 180),
}

IDENTIFICATION = { "title": "SciELO - Scientific Electronic Library On-line",
                   "sub_title": "SciELO Brasil",
                   "address": "Rua Diogo de Farias, 1087 conj. 810 - Vila Clementino",
                   "cep": "04037-000",
                   "country": "Brasil",
                   "state": "São Paulo",
                   "city": "São Paulo",
                   "phone": "+ 55 11 3369-4080",
                   "fax": "+ 55 11 3369-4080",
                   "mail": "scielo@scielo.org"
}

COUCHDB_VIEWS = { "sci_alphabetic": DB_SERVER+DB_NAME+"/_design/couchdb/_view/title_id?include_docs=true",
                  "sci_serial": DB_SERVER+DB_NAME+"/_design/couchdb/_view/title_id?include_docs=true&key=\"{pid}\"",
                  "sci_issues": DB_SERVER+DB_NAME+"/_design/couchdb/_view/issues_id?include_docs=true",
                  "sci_issuetoc": DB_SERVER+DB_NAME+"/_design/couchdb/_view/issues_id/{pid}?include_docs=true",
                  "sci_abstract": DB_SERVER+DB_NAME+"/_design/couchdb/_view/article_id/{pid}?include_docs=true",
                  "sci_arttext": DB_SERVER+DB_NAME+"/_design/couchdb/_view/article_id/{pid}?include_docs=true",
}

COUCHDB_QUERIES = { "journal_pressrelases": DB_SERVER+DB_NAME+"/_design/couchdb/_view/article_pr?descending=true&limit="+str(LIMIT),
                    "journal_lastarticles": DB_SERVER+DB_NAME+"/_design/couchdb/_view/article?descending=true&limit="+str(LIMIT)
}

# Website Configurations

WS_CONFIG = { "identity" : {"title": "SciELO Brasil",}}