#!/bin/bash




if [ `ls / | grep "root" | wc -l` -eq 1 ] ; then #root의 .bashrc 설정 환경변수
    echo "root"
    root_env_num=`awk -F '=' '/^export/' /root/.bashrc | wc -l`
    echo $root_env_num
    root_env_list=`awk -F '=' '/^export/' /root/.bashrc`
    echo $root_env_list
else
    echo "root가 없음!"
fi

if [ `ls / | grep "root" | wc -l` -eq 1 ] ; then #root의 .profile 설정 환경변수
    echo "root"
    root_env_num=`awk -F '=' '/^export/' /root/.profile | wc -l`
    echo $root_env_num
    root_env_list=`awk -F '=' '/^export/' /root/.profile`
    echo $root_env_list
else
    echo "root가 없음!"
fi

