function(doc) {
  // !code _attachments/js/includes.js

  if (doc.v706[0]["_"] == 'i'){
     emit(doc.v35[0]["_"]+doc.v36[0]["_"].substr(0,4)+PadDigits(doc.v36[0]["_"].substr(4,1),4), null);
  }
}