function(doc) {

  if (doc.v706 == 'network'){
     emit([doc.status,doc.acron],doc);
  }
}