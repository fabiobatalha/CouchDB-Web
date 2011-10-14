function(doc) {
  if (doc.v706["0"]["_"].toUpperCase() === "T"){
    if (doc.v50["0"]["_"].toUpperCase() === "C"){
      emit(doc.v100[0]["_"], null);
    }
  }
}