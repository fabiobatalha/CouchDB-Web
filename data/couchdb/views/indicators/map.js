function(doc) {
    if (doc.v706["0"]["_"].toUpperCase() === "T"){
        if (doc.v50["0"]["_"].toUpperCase() === "C"){
            if ( doc.v51 ){
                if (! doc.v51["0"]["d"]){
                    emit([doc.v980[0]["_"],doc.v706[0]["_"]], 1);
                }
             }else{
                 emit([doc.v980[0]["_"],doc.v706[0]["_"]], 1);
             }
        }
    }else{
        emit([doc.v980[0]["_"],doc.v706[0]["_"]], 1);
    }
}