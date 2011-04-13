DEBUG     = True
DB_SERVER = 'http://teste.webservices.scielo.org/'
DB_NAME   = 'scielobr1'
LIMIT     = 10
LANG      = 'pt'

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
                   "state": "Sao Paulo",
                   "city": "Sao Paulo",
                   "phone": "+ 55 11 3369-4080",
                   "fax": "+ 55 11 3369-4080",
                   "mail": "scielo@scielo.org"
}

COUCHDB_VIEWS = { "sci_alphabetic": DB_SERVER+DB_NAME+"/_design/couchdb/_view/title?include_docs=true",
                  "sci_serial": DB_SERVER+DB_NAME+"/_design/couchdb/_view/title_id?include_docs=true&key=\"{pid}\"",
                  "sci_issue": DB_SERVER+DB_NAME+"/_design/couchdb/_view/issue_id?include_docs=true&key=\"{pid}\"",
                  "sci_issues": DB_SERVER+DB_NAME+"/_design/couchdb/_view/issue_id?include_docs=true&startkey=\"{pid}\\u9999\"&endkey=\"{pid}\"&descending=true",
                  "sci_issuetoc": DB_SERVER+DB_NAME+"/_design/couchdb/_view/article_id/?include_docs=true&startkey=\"S{pid}\"&endkey=\"S{pid}\\u9999\"",
                  "sci_article": DB_SERVER+DB_NAME+"/_design/couchdb/_view/article_id/?include_docs=true&key=\"{pid}\"",
}

COUCHDB_QUERIES = { "journal_pressreleases": DB_SERVER+DB_NAME+"/_design/couchdb/_view/article_pr?include_docs=true&limit="+str(LIMIT)+"&startkey=[\"{pid}\",{brac}]&endkey=[\"{pid}\"]&descending=true",
                    "journal_lastarticles": DB_SERVER+DB_NAME+"/_design/couchdb/_view/article?include_docs=true&limit="+str(LIMIT)+"&startkey=[\"{pid}\",{brac}]&endkey=[\"{pid}\"]&descending=true",
                    "issues_count_pid":     DB_SERVER+DB_NAME+"/_design/couchdb/_view/issue_count?key=[\"{pid}\"]&group=true",
                    "issues_count_all":     DB_SERVER+DB_NAME+"/_design/couchdb/_view/issue_count?group=true",
}

# Website Configurations

WS_CONFIG = { "identity" : {"title": "SciELO Brasil","doi_prefix":"10.1590"}}