#!/bin/bash

function check_print_and_clear()
{
    if [ x"$1" != x ]
    then
##        echo "$name : $stat $lstate $astate $sstate $priority $nicev | $pid | $uid | $names"
#        echo "$name | $stat | $pid | $uid | $priority | $nicev | $desc | $lstate | $astate | $sstate | $id | $names"
        echo "$name | $stat | $typev"
        pid=""
        uid=""
        priority=""
        nicev=""
        desc=""
        lstate=""
        astate=""
        sstate=""
        id=""
        names=""
        typev=""
    fi
}

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
            name=`echo "$name" | sed 's/\@\./\@\*\./g'`
            res=`systemctl show -- "$name"`
            name=`echo "$name" | sed 's/\@\*\./\@\./g'`
            if [ x"$res" == x ]
            then
                name=`echo "$name" | sed 's/\@\./\@123123\./g'`
                res=`systemctl show -- "$name"`
                name=`echo "$name" | sed 's/\@123123\./\@\./g'`
            fi
            while read element
            do
                case $element in
                    MainPID=*)
                        check_print_and_clear "$pid"
                        pid=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    UID=*)
                        check_print_and_clear "$uid"
                        uid=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    CPUSchedulingPriority=*)
                        check_print_and_clear "$priority"
                        priority=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    Nice=*)
                        check_print_and_clear "$nicev"
                        nicev=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    Description=*)
                        check_print_and_clear "$desc"
                        desc=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    LoadState=*)
                        check_print_and_clear "$lstate"
                        lstate=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    ActiveState=*)
                        check_print_and_clear "$astate"
                        astate=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    SubState=*)
                        check_print_and_clear "$sstate"
                        sstate=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    Id=*)
                        check_print_and_clear "$id"
                        id=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    Names=*)
                        check_print_and_clear "$names"
                        names=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    Type=*)
                        check_print_and_clear "$typev"
                        typev=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                esac
            done < <(echo "$res"
            check_print_and_clear "$names")
        else
            res=`systemctl show -- "$name"`
            while read element
            do
                case $element in
                    MainPID=*)
                        pid=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    UID=*)
                        uid=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    CPUSchedulingPriority=*)
                        priority=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    Nice=*)
                        nicev=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    Description=*)
                        desc=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    LoadState=*)
                        lstate=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    ActiveState=*)
                        astate=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    SubState=*)
                        sstate=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    Id=*)
                        id=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    Names=*)
                        names=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                    Type=*)
                        typev=`echo "$element" | awk -F '=' '{print $2}'`
                        ;;
                esac
            done < <(echo "$res")
        fi
        check_print_and_clear "1"
    fi
done
