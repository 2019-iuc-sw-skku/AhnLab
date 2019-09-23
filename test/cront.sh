#!/bin/bash

cat /etc/passwd | while read line
do
    name=${line%%:*}
#    echo $name
    crontab -u $name -l
done
