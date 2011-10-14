#
#This script checks if the documents exist in couchDB and delete all title and issues documents
#

. scielo2couchdb_config.sh

for databases in `find $serial_dir | grep .mst`
do

	if [ $databases != $serial_dir"/title/title.mst" ] && [ $databases != $serial_dir"/issue/issue.mst" ] 
		then
			echo "---+--- PROCESS DATABASE: " $databases
			$cisis_dir/mx $databases "pft=v880/" -all now > ../output/pid.txt
			python ../lib/couchcmdtools/delete.py -s $couchdb_url -d $couchdb_database -v article_id  -in ../output/pid.txt
	fi

done

#Delete title|issue from couchdb
echo "---+--- DELETE TITLE ON COUCHDB (TITLE_ID VIEWER)"
python ../lib/couchcmdtools/delete.py -v title_id -d $couchdb_database -s $couchdb_url

echo "---+--- DELETE ISSUE ON COUCHDB (ISSUE_ID VIEWER)"
python ../lib/couchcmdtools/delete.py -v issue_id  -d $couchdb_database -s $couchdb_url

echo "---+--- DELETE NETWORK ON COUCHDB (NETWORK VIEWER)"
python ../lib/couchcmdtools/delete.py -v network  -d $couchdb_database -s $couchdb_url

rm -f pid.txt
