#!/bin/bash

function find_real()
{
    if [ -L "$1" ]
    then
        lpath=`ls -l $1`
        lpath=${lpath##* }
        find_real $lpath
    else
        echo $1
    fi
}
for i in $@
do
    res=`find_real $i`
    if [ $res != $i ]
    then
        echo $i $res
    fi
done
