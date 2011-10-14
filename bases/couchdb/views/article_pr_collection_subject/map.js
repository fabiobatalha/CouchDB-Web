function(doc) {

  if (doc.v706[0]["_"] == 'h' && doc.v41[0]["_"] =="pr" ){
     emit([doc.v980[0]["_"],doc.v966[0]["_"],doc.v65[0]["_"]],{"collection":doc.v980[0]["_"], 
                                                "pid":doc.v880[0]["_"],
                                                "article_title":doc.v12,
                                                "pubdate":doc.v65,
                                                "author":doc.v10,
                                                "affiliation":doc.v70,
                                                "abstract":doc.v83,
                                                "journal":doc.v30,
                                                "issn":doc.v35,
                                                "vol": doc.v31,
                                                "num":doc.v32,
                                                "vol_suppl":doc.v131,
                                                "num_suppl":doc.v132,
                                                "original_language":doc.v40,                                                
                                                "url": "http://"+collections_list[doc.v980[0]["_"]].domain+
          "/scielo.php?script=sci_arttext_pr&pid="+doc.v880[0]["_"]+"&lng=en&nrm=iso"
                                        });
  }
}