. scielo2couchdb_config.sh

i=0

for collection in `ls -1 $database_dir"/input/iso/"`
do
    error="false"
    echo "MANIPULATING $collection DATA"
    echo "--- CREATING DIRECTORY TO RECEIVE MASTER FILES FROM "$collection" DATABASE TITLE.ISO"
    echo "---+--- mkdir -p ../input/"$collection
    mkdir -p ../input/$collection

    echo "--- VERIFIING IF TITLE.ISO EXISTS"
    title_iso=$database_dir"input/iso/"$collection"/title.iso"
    if [ -f  $title_iso ]; then
        echo "---+--- YES TITLE.ISO EXISTS"    
        echo "--- CREATING MASTER FROM "$collection" DATABASE TITLE.ISO"
        echo "---+--- "$cisis_dir"/mx iso="$title_iso" create=../input/"$collection"/title -all now"
        $cisis_dir/mx iso=$title_iso create=../input/$collection/title -all now       
    else
        echo "---+--- [ERROR] TITLE.ISO DOESN'T EXISTS"
        error="true"
    fi
    echo "--- VERIFIING IF TITLE.MST and TITLE.XRF EXISTS"
    if [ -f  ../input/$collection/title.mst ]; then
        echo "---+--- YES TITLE.MST EXISTS"        
    else
        echo "---+--- [ERROR] TITLE.MST DOESN'T EXISTS"
        error="true"
    fi
    if [ -f  ../input/$collection/title.xrf ]; then
        echo "---+--- YES TITLE.XRF EXISTS"        
    else
        echo "---+--- [ERROR] TITLE.XRF DOESN'T EXISTS"
        error="true"
    fi
    echo "--- INDEXING TITLE"   
    if [ $error = "false" ]; then
        echo '---+---' $cisis_dir/mx ../input/$collection/title "\"fst='1 0 |ISSN=|v400,/'\"" fullinv=../input/$collection/title
        $cisis_dir/mx ../input/$collection/title "\"fst='1 0 |ISSN=|v400,/'\"" fullinv=../input/$collection/title
        echo "---+--- INDEX DONE"            
    else
        echo "---+--- [ERROR] INDEX FAIL"
        error="true"
    fi
done
