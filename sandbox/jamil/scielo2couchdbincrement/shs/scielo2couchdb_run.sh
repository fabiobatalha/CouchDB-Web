
. scielo2couchdb_config.sh

#Início do processamento incremental couchdb

echo "APPEND DATABASES"
./scielo2couchdb_append_databases.sh

#echo "RUNNING BULKUP"
./scielo2couchdb_bulkup.sh
