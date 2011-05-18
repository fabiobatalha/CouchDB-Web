
. scielo2couchdb_config.sh

database="serial"
ISOFILE="serial.iso"

echo "Counting registers in "$database
total=`$cisis_dir/mx $database pft=mfn/ now | wc -l`

echo "Bulking $total registers - Be calm, this process could take a while!"

i=0

while [ $i -le $total ]
	do
		python ../lib/isis2couchdb/tools/isis2json.py $ISOFILE -c -q $bulk_size -s $i -u -p v -t 3 | curl -d @- -H "Content-Type: application/json" -X POST $couchdb_database/_bulk_docs
		
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

echo "Finish the process";
