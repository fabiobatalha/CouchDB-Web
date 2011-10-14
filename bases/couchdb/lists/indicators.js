function(head, req) {
    // !json templates.indicators
    // !code _attachments/js/collections_list.js

    var chart1; // globally available
    var Mustache = require('vendor/couchapp/lib/mustache');
    var register = null;
    var body = null;
    var post = new Array();
    var collections = new Array();
    var types = new Array();
    var series = new Object();
    series.i = new Array;
    series.t = new Array;
    series.h = new Array;

    start({
        "headers": {
            "Content-Type": "text/html"
        }
    });

    function custLog(x,base) {
	// Created 1997 by Brian Risk.  http://brianrisk.com
	return (Math.log(x))/(Math.log(base));
    }


    Array.prototype.getUniqueValues = function () {
        var hash = new Object();
        for (j = 0; j < this.length; j++) {hash[this[j]] = true}
        var array = new Array();
        for (value in hash) {array.push(value)};
        return array;
   }

    while (row = getRow()) {
      if (collections_list[row.key[0]]){
          collections.push(collections_list[row.key[0]]['name']['en']);
      }else{
          collections.push(row.key[0]);
      }
      types.push(row.key[1]);
      post.push(row.value);

      if (row.key[1] == "i"){
         series.i.push(custLog(row.value,10));
      }else if (row.key[1] == "h"){
         series.h.push(custLog(row.value,10));
      }else if (row.key[1] == "t"){
         series.t.push(custLog(row.value,10));
      }

    }

    var chart_params =  {
        categories: collections.getUniqueValues(),
        series: []
    }

   chart_params.series.push({name: "issues", data: series.i });
   chart_params.series.push({name: "articles", data: series.h });
   chart_params.series.push({name: "titles", data: series.t });


    var myJSONText = JSON.stringify(chart_params);

    registers = {"rows" : myJSONText };
    return Mustache.to_html(templates.indicators,registers);

}