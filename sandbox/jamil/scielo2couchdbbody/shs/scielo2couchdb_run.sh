. scielo2couchdb_config.sh

echo "RUNING DATABASES"
./scielo2couchdb_database.sh

echo "RUNNING BULKUP"
./scielo2couchdb_bulkup.sh
