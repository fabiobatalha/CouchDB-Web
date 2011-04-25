#!/bin/bash
MFN=$1
PID=$2

mx null count=1 "pft='!ID ','$MFN'/" now >>pid_id.txt
mx artigo count=1 btell=0 bool="ART=$PID" pft=@v880.pft lw=1000 -all now >>pid_id.txt
mx artigo btell=0 bool="ART=$PID" pft=@v704.pft lw=1000 -all now >>pid_id.txt

