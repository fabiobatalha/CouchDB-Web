#!/bin/bash
MFN=$1
PID=$2
LINDG4=/usr/local/bireme/cisis/5.5.pre02/linux/lindG4

$LINDG4/mx null count=1 "pft='!ID ','$MFN'/" now >>pid_id.txt

$LINDG4/mx ../base_20110412/artigo count=1 btell=0 bool="ART=$PID" pft=@v880.pft lw=1000 -all now >>pid_id.txt

echo '!v704!' >> pid_id.txt

$LINDG4/mx ../base_20110412/artigo btell=0 bool="ART=$PID" pft=@v704.pft lw=1000 -all now >>pid_id.txt
