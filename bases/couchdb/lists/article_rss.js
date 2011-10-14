function(head, req) {
    // !json templates.articles_rss
    // !code _attachments/js/config.js
    // !code _attachments/js/collections_list.js

    var Mustache = require('vendor/couchapp/lib/mustache');
    var register = null;
    var body = null;
    start({
        "headers": {
            "Content-Type": "text/xml"
        }
    });    
    
    var post = new Array();


    while (row = getRow()) {
        row.value["collection_info"] = collections_list[row.value["collection"]];
        row.value["article_url"] = "http://"+collections_list[row.value.collection].domain+
            "/scielo.php?script=sci_arttext&pid="+row.value.pid+"&lng="+
            req.query.lang+"&nrm=iso&tlng=en" ;

        // Choosing the title language according to the paramenter lang
        for (i in row.value.article_title){
            if (row.value.article_title[i].l === req.query.lang){
                row.value["article_req"] = row.value.article_title[i]._;
                break;
            }else{
                row.value["article_req"] = row.value.article_title[i]._;
            }
        }

        // Choosing the abstract language according to the paramenter lang
        for (i in row.value.abstract){
            if (row.value.abstract[i].l === req.query.lang){
                row.value["abstract_req"] = row.value.abstract[i].a;
                break;
            }else{
                row.value["abstract_req"] = row.value.abstract[i].a;
            }
        }

        post.push(row.value);
    }

    registers = {"rows" : post };
    return Mustache.to_html(templates.articles_rss,registers);
    
}