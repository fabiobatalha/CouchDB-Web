function(doc) {
  if (doc.v706["0"]["_"].toUpperCase() === "T"){
    if (doc.v50["0"]["_"].toUpperCase() === "C"){
      if ( doc.v51 ){
        if (! doc.v51["0"]["d"]){
          emit(doc.v400[0]["_"], null);
        }
      }else{
        emit(doc.v400[0]["_"], null);
      }
    }
  }
}