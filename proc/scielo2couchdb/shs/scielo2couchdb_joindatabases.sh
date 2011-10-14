. scielo2couchdb_config.sh

# LISTING CONTENT IN the input/iso directory to get the collections and databases available to append in a global database.

#databases=`echo "artigo issues title bib4cit"`
#for files in $databases
#do
echo "--- CREATING EMPTY DATABASES FOR ARTICLE, ISSUE, TITLE and CITATIONS"
echo "---+--- mkdir -p ../output"
mkdir -p ../output
echo "---+--- $cisis_dir/mx null count=0 create=../output/artigo"
$cisis_dir/mx null count=0 create=../output/artigo
echo "---+--- $cisis_dir/mx null count=0 create=../output/issues"
$cisis_dir/mx null count=0 create=../output/issues
echo "---+--- $cisis_dir/mx null count=0 create=../output/title"
$cisis_dir/mx null count=0 create=../output/title
echo "---+--- $cisis_dir/mx null count=0 create=../output/bib4cit"
$cisis_dir/mx null count=0 create=../output/bib4cit
echo "--- APPENDING FILES"
for collection in `ls -1 $database_dir"/input/iso/"`
do
   for file in `ls -1 $database_dir"/input/iso/$collection/"`
   do
        file_iso=$database_dir"/input/iso/"$collection"/"$file
        proc=""
        procb=""
        if [ $file == "artigo.iso" ]
        then
            echo "---+--- artigo.iso from "$collection
            proc="proc='a980#$collection#'"
            echo "---+--- INCLUDING JOURNAL DATA INSIDE ARTICLE REGISTER 'SUBJECT'"
            procb="proc=ref(['../input/$collection/title']l(['../input/$collection/title'],s('ISSN=',v35)),('a966#',v441,'#'))"
            
        elif [ $file == "title.iso" ]
        then
            echo "---+--- title.iso from "$collection
            proc="proc='a706#t#a980#$collection#'" 
        elif [ $file == "issues.iso" ]
        then
            echo "---+--- issues.iso from "$collection
            proc="proc='a980#$collection#'"
        elif [ $file == "bib4cit.iso" ]
        then
            echo "---+--- bib4cit.iso from "$collection
            proc="proc='a980#$collection#'"
        fi
     
        if [ -f $file_iso ]
        then
            echo "---+---" $cisis_dir/mx iso=$file_iso $proc $procb append=../output/${file/.iso} -all now
            $cisis_dir/mx iso=$file_iso $proc $procb append=../output/${file/.iso} -all now
        else
            echo "---+--- [ERROR] FILE DOESN'T EXISTS: "$file_iso
        fi
    done
done

for database in `ls -1 ../output/*.mst`
do
    echo "---+--- CONVERTING JOINED DATABASE $database TO ISO"
    echo $cisis_dir"/mx" ${database/.mst} "iso="${database/.mst}".iso -all now"
    $cisis_dir/mx ${database/.mst} iso=${database/.mst}.iso -all now
done
rm ../output/*.mst
rm ../output/*.xrf
