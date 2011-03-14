function(head, req) {
    // !json templates.indicators_title_subject_collections
    // !code _attachments/js/config.js
    // !code _attachments/js/collections_list.js

    var chart1; // globally available
    var Mustache = require('vendor/couchapp/lib/mustache');
    var register = null;
    var body = null;
    var post = new Array();
    var series = new Object();
    var data = new Array();
    var total = null;

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
        if (! series[row.key[1]]){
            series[row.key[1]] = null;
            series[row.key[1]] += eval(row.value);
        }else{
            series[row.key[1]] += eval(row.value);
        }
        total += eval(row.value);
    }

    for (i in series){
       data.push(Array(i,series[i]));
    }

    var chart_params =  {data: data, total: total};

    var myJSONText = JSON.stringify(chart_params);

    registers = {"rows" : myJSONText};
    return Mustache.to_html(templates.indicators_title_subject_collections,registers);


}