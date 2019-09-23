#!/bin/bash

rm -f result
for i in {1..10}
do
    echo "result $i"
    res=`./services.py`
    echo $res
    echo $res >> result
done
