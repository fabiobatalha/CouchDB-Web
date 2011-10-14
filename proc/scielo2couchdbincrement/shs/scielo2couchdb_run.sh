#
#Start incremental process couchDB
#
#IMPORTANT: Database issue e title are full data.
#
#Step 1: verifiy if is a update or insert and delete all issue/title
#
#Step 2: append the databases 
#
#Step 3: send to couchdb (Bulk)

. scielo2couchdb_config.sh

echo "[ACTIVATING VIRTUAL ENVIRONMENT]"
source ../../services-env/bin/activate

echo "---+--- CHECKING UPDATE DOCUMENTS"
./scielo2couchdb_check_update.sh

echo "---+--- APPEND DATABASES"
./scielo2couchdb_append_databases.sh

echo "---+--- RUNNING BULKUP"
./scielo2couchdb_bulkup.sh
