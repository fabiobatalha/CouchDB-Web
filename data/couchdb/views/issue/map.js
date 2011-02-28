function(doc) {
  // !code _attachments/js/includes.js
  // !code _attachments/js/collections_list.js

  if (doc.v706[0]["_"] == 'i'){
     emit([doc.v980["0"]["_"],doc.v91["0"]["_"]], {"collection":doc.v980["0"]["_"],"issn":doc.v35[0]["_"],"title": doc.v130[0]["_"],"publisher": doc.v480[0],"insert_date":doc.v91[0]["_"],"vol":doc.v31[0]["_"],"num":doc.v32[0]["_"],"url": "http://"+collections_list[doc.v980[0]["_"]].domain+
          "/scielo.php?script=sci_issuetoc&pid="+doc.v35[0]["_"]+doc.v36[0]["_"].substr(0,4)+PadDigits(doc.v36[0]["_"].substr(4,1),4)+"&lng=en&nrm=iso"});

  }
}
//         "legend": doc.v43,
