#!/bin/bash
stime=$(date +%s%N)
resstr=""
for i in $@
do
    path=$i
    statres=`stat -c "%x | %y" $i 2>/dev/null`
    accdate=${statres%% | *}
    moddate=${statres##* | }
    accdate=${accdate%%.*}
    moddate=${moddate%%.*}
    md5=`md5sum $i 2>/dev/null`
    md5=${md5%% *}
    sha256=`sha256sum $i 2>/dev/null`
    sha256=${sha256%% *}
    resstr="$resstr$path | $accdate | $moddate | $md5 | $sha256\n"
done
echo -e $resstr
etime=$(date +%s%N)
elapsed=`echo "($etime - $stime) / 1000000" | bc`
elapsedSec=`echo "scale=6;$elapsed / 1000" | bc | awk '{printf "%.6f", $1}'`
#echo TOTAL: $elapsedSec sec
