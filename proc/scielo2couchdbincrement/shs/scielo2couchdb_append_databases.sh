#
# LISTING CONTENT IN the serial directory to get the collections and databases available to append in a global database.
#
. scielo2couchdb_config.sh

$cisis_dir/mx null count=0 create=serial

for databases in `find $serial_dir | grep .mst`
do
 	
	if [ $databases != $serial_dir"/title/title.mst" ] && [ $databases != $serial_dir"/issue/issue.mst" ] 
		then
		if [ -f $databases ]
			then
				$cisis_dir/mx $databases $proc append=serial -all now
			else
				echo "---+--- [ERROR] file doesnt exist: "$databases
		fi
	fi
done

echo "---+--- PROCESS TITLE"
proc="proc='a706#t#a980#sci#'"
$cisis_dir/mx $serial_dir/"title/title.mst" $proc append=serial -all now

echo "---+--- PROCESS ISSUE"
proc="proc='a980#sci#'"
$cisis_dir/mx $serial_dir/"issue/issue.mst" $proc append=serial -all now

echo "---+--- GERANATE ISO FILE";
$cisis_dir/mx serial iso=serial.iso -all now

