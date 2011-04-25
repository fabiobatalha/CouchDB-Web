#!/bin/bash
echo \!ID 000000001>>pid_id.txt
mx artigo count=1 btell=0 bool="ART=S1519-566X2008000600012" pft=@v880.pft lw=1000 -all now >>pid_id.txt
mx artigo btell=0 bool="ART=S1519-566X2008000600012" pft=@v704.pft lw=1000 -all now >>pid_id.txt

