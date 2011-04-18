#!/bin/sh

. ./scielo2couchdb_config.sh

	echo "Sending the records to couchdb: "$couchdb_database

    MSTFILE=$database_dir/output/mst/org$database_name".mst"
    echo "Counting registers in: "org$database_name".mst"
    total=$($cisis_dir/mx $database_dir/output/mst/org$database_name".mst" pft=mfn/ now | wc -l)
     
    echo "Bulking $total registers - Be calm, this process could take a while!"
    
	i=0
	while [ $i -le $total ]
    do
       $jython_path -J-Xms2048m -J-Xmx2048m ../lib/isis2couchdb/tools/isis2json.py $MSTFILE -c -q $bulk_size -s $i -u -p v -t 3 | curl -d @- -H "Content-Type: application/json" -X POST $couchdb_database/_bulk_docs

        if [ $(($i + $bulk_size)) -ge $total ]
        then
            tmp=$(($i - $bulk_size))
            bulk_size=$(($total - $tmp))
            echo "done from "$i" to " $total
            break 1
        else
            echo "done from "$i" to " `expr $i + $bulk_size`
            i=$(($i + $bulk_size))
        fi
    done
