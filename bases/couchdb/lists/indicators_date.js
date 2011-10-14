function(head, req) {
    // !json templates.indicators_date
    // !code _attachments/js/collections_list.js

    var chart1; // globally available
    var Mustache = require('vendor/couchapp/lib/mustache');
    var register = null;
    var body = null;
    var post = new Array();
    var collections = new Array();
    var category = null;
    var categories = new Array();
    var xAxis = new Object();
    var types = new Array();
    var series = new Object();

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
      //categories
      xAxis[row.key[2].substr(0,4)] = null;

      category = row.key[2].substr(0,4);
      if (! series[category]){
          series[category] = {"i":null,"h":null,"t":null};
      }
      if (row.key[1] == "i"){
        series[category]["i"] += eval(row.value);
      }else if (row.key[1] == "h"){
        series[category]["h"] += eval(row.value);
      }else if (row.key[1] == "t"){
        series[category]["t"] += eval(row.value);
      }
   }

    for (category in xAxis){
        //Creating categories array
        categories.push(category);
    }
    sorted_categories = categories.sort();

    var sorted_series = new Object();
    sorted_series["series"] = new Object();
    sorted_series["series"]["i"] = new Array();
    sorted_series["series"]["h"] = new Array();
    sorted_series["series"]["t"] = new Array();

    for (cat in sorted_categories){
        vali = eval(series[sorted_categories[cat]]["i"]);
        valh = eval(series[sorted_categories[cat]]["h"]);
        valt = eval(series[sorted_categories[cat]]["t"]);
        sorted_series["series"]["i"].push(vali);
        sorted_series["series"]["h"].push(valh);
        sorted_series["series"]["t"].push(valt);
    }

    series = new Array();
    var i = 0;
    for (serie in sorted_categories){
        series.push({"name": serie, "data": sorted_series["series"][i]});
        i += i;
    }

    var chart_params =  {
        categories: sorted_categories,
        series: sorted_series
    }

    var myJSONText = JSON.stringify(chart_params);

    registers = {"rows" : myJSONText};
    return Mustache.to_html(templates.indicators_date,registers);

}
