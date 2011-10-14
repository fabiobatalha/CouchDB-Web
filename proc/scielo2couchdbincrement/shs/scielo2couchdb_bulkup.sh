. scielo2couchdb_config.sh

database="serial"
ISOFILE="serial.iso"

echo "---+--- Counting registers in "$database
total=`$cisis_dir/mx $database pft=mfn/ now | wc -l`

echo "---+--- Bulking $total registers - Be calm, this process could take a while!"

i=0

while [ $i -le $total ]
	do
		../lib/isis2couchdb/tools/isis2json.py $ISOFILE -c -q $bulk_size -s $i -u -p v -t 3 | curl -d @- -H "Content-Type: application/json" -X POST $couchdb_url$couchdb_database/_bulk_docs

	if [ $(($i + $bulk_size)) -ge $total ]
		then
		tmp=$(($i - $bulk_size))
		bulk_size=$(($total - $tmp))
		echo "---+--- DONE FROM "$i" TO " $total
	break 1
	else
		echo "---+--- DONE FROM "$i" TO " `expr $i + $bulk_size`
		i=$(($i + $bulk_size))
	fi
done

rm -f serial.*

echo "---+--- PUTTING NETWORK JSON TO THE COUCHDB DATABASE"
cat $input_dir/network/network.json | curl -d @- -H "Content-Type: application/json" -X POST $couchdb_url$couchdb_database/_bulk_docs

#echo "---+--- PUSHING COUCHAPP TO THE COUCHDB DATABASE"
#cd $input_dir/couchdb
#couchapp push $couchdb_database 
#cd -

echo "---+--- FINISH PROCESS";
