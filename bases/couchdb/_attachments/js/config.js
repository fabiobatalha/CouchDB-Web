config = {"lang": "en"}


if (! req.query.lang){
    req.query.lang = config.lang;
}