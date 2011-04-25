#!/bin/bash
MFN=1
PID=S0044-59672009000200001

mx null count=1 "pft='!ID ','$MFN'/" now >>tes.txt

mx ../base_20110412/artigo count=1 btell=0 bool="ART=$PID" pft=@v880.pft lw=1000  now >>tes.txt

echo '!v704!' >>tes.txt

mx ../base_20110412/artigo btell=0 bool="ART=$PID" pft=@v704.pft lw=1000 now >>tes.txt

