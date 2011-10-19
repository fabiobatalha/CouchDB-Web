function(head, req) {
    // !json templates.titles_rss
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
      row.value["collection_info"] = collections_list[row.value.collection];
      row.value["title_url"] = "http://"+collections_list[row.value.collection].domain+
          "/scielo.php?script=sci_serial&pid="+row.value.issn+"&lng="+req.query.lang+
          "&nrm=iso";
      post.push(row.value);
    }


    registers = {"rows" : post };
    return Mustache.to_html(templates.titles_rss,registers);

}