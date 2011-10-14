function(doc) {
  function PadDigits(n, totalDigits){
    n = n.toString();
    var pd = '';
    if (totalDigits > n.length) {
        for (i=0; i < (totalDigits-n.length); i++){
            pd += '0';
        }
    }
    return pd + n.toString();
  }

  if (doc.v706[0]["_"] == 'i'){
    emit(doc.v35[0]["_"], 1);
  }
}