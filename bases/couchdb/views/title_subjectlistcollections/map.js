function(doc) {

  if (doc.v706[0]["_"] == 't'){

     for (i in doc.v441){
         emit([doc.v980["0"]["_"], doc.v441[i]["_"]],1);
     }

  }

}