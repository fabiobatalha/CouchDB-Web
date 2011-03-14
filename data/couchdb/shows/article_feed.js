function(doc, req) {
    // !json templates.abs

    var Mustache = require('vendor/couchapp/lib/mustache');
    var register = null;

    register = {"article_title":doc.v12[0]["_"]};
    return Mustache.to_html(templates.abs,register);
}
