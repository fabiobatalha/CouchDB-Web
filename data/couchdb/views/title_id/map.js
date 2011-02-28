function(doc) {
  if (doc.v706[0]["_"] == 't'){
     emit(doc.v400[0]["_"], null);
  }
}