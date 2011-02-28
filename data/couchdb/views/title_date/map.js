function(doc) {
  // !code _attachments/js/collections_list.js

  if (doc.v706[0]["_"] == 't'){
     subjects = new Array();

     for (i in doc.v441){
         subjects.push(doc.v441[i]["_"]);
     }

     emit(doc.v942[0]["_"], {"collection":doc.v980["0"]["_"],
         "issn":doc.v400[0]["_"],
         "title": doc.v100[0]["_"],
         "subject": subjects,
         "publisher": doc.v480[0],
         "insert_date":doc.v942[0]["_"],
         "url": "http://"+collections_list[doc.v980[0]["_"]].domain+
          "/scielo.php?script=sci_serial&pid="+doc.v400[0]["_"]+"&lng=en&nrm=iso"
     });
  }
}