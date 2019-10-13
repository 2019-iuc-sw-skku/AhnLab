#!/bin/bash

field=0

list=`systemctl list-unit-files --no-legend --no-pager`
for line in $list
do
    if [ $field -eq 0 ]
    then
        name=`echo "$line" | sed -e 's/^ *//g' -e 's/ *$//g'`
        field=1
    else
        stat=`echo "$line" | sed -e 's/^ *//g' -e 's/ *$//g'`
        field=0

        if [[ "$name" =~ "@" ]]
        then
            res=`systemctl show -- "$name"1`
#            name="$name"1
        else
            res=`systemctl show -- "$name"`
#            name=$name
        fi
        pid=`echo "$res" | grep ^MainPID= | awk -F '=' '{print $2}'`
        uid=`echo "$res" | grep ^UID= | awk -F '=' '{print $2}'`
        priority=`echo "$res" | grep ^CPUSchedulingPriority= | awk -F '=' '{print $2}'`
        nicev=`echo "$res" | grep ^Nice= | awk -F '=' '{print $2}'`
        desc=`echo "$res" | grep ^Description= | awk -F '=' '{print $2}'`
        loadstate=`echo "$res" | grep ^LoadState= | awk -F '=' '{print $2}'`
        activestate=`echo "$res" | grep ^ActiveState= | awk -F '=' '{print $2}'`
        substate=`echo "$res" | grep ^SubState= | awk -F '=' '{print $2}'`
        id=`echo "$res" | grep ^Id= | awk -F '=' '{print $2}'`
        names=`echo "$res" | grep ^Names= | awk -F '=' '{print $2}'`
#        pid=`systemctl show -- "$name" | grep ^MainPID= | awk -F '=' '{print $2}'`
#        uid=`systemctl show -- "$name" | grep ^UID= | awk -F '=' '{print $2}'`
#        priority=`systemctl show -- "$name" | grep ^CPUSchedulingPriority= | awk -F '=' '{print $2}'`
#        nicev=`systemctl show -- "$name" | grep ^Nice= | awk -F '=' '{print $2}'`

#        echo "$name : $stat - [pid]$pid / [uid]$uid"
        if [ "$id" != "$names" ]
        then
            echo "$name : $id | $names" # $stat $loadstate $activestate $substate"
        fi
    fi

done
