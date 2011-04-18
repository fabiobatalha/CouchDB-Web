. scielo2couchdb_config.sh


	database=$database_name
	collection=`echo "body"`

	echo "Create empty database org"$database

	$cisis_dir/mx null count=0 create=org$database

	echo "Get imput file on: "$database_dir"input/mst/"$database".mst"

	file=$database_dir"input/mst/"$database".mst"

	echo "Add Type on 706=b(body) and Collection on 980=(body)"

	proc="proc='a706#b#a980#$collection#'"

	echo "Append database, wait...."

		if [ -f $file ]
		then
			$cisis_dir/mx $file $proc append=orgbody -all now
		else
			echo "[ERROR]: file on: "$file"doesnt exist: "
		fi

	echo "Create folder: " $database_dir"output/mst"
	mkdir -p $database_dir"output/mst"
	
	echo "Move file: *.mst to: " $database_dir"output/mst"
	mv *.mst $database_dir"output/mst"
	echo "Move file: *.xrf to: " $database_dir"output/mst"
	mv *.xrf $database_dir"output/mst"
