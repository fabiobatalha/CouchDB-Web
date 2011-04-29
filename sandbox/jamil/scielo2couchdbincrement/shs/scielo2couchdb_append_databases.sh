. scielo2couchdb_config.sh

# LISTING CONTENT IN the serial directory to get the collections and databases available to append in a global database.

$cisis_dir/mx null count=0 create=serial

for databases in `find $serial_dir | grep .mst`
do
 	if [ $databases == $serial_dir/"title.mst" ]
		then
		   echo "proc title"
		   proc="proc='a706#t#a980#title#'"
		elif [ $databases == $serial_dir/"issue.mst" ]
		then
		   echo "proc issue"
		   proc="proc='a980#$issue#'"
	fi
		   		   
	if [ -f $databases ]
       then
           $cisis_dir/mx $databases append=serial -all now
       else
			echo "[ERROR] file doesnt exist: "$file
    fi
done
