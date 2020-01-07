#!/bin/bash

usernum=`ls /home | wc -l`
echo $usernum
if [ $usernum -ne 0 ] ;then
    for user_name in `ls /home` #일반 사용자의 .bashrc 설정 환경변수
        do
            echo $user_name
            user_env_num=`awk -F '=' '/^export/' /home/$user_name/.bashrc | wc -l`
            echo $user_env_num
            user_env_list=`awk -F '=' '/^export/' /home/$user_name/.bashrc`
            echo $user_env_list
        done


    for user_name in `ls /home` #일반 사용자의 .profile 설정 환경변수
        do
            echo $user_name
            user_env_num=`awk -F '=' '/^export/' /home/$user_name/.profile | wc -l`
            echo $user_env_num
            user_env_list=`awk -F '=' '/^export/' /home/$user_name/.profile`
            echo $user_env_list
        done
else
    echo "일반 사용자 없음"
fi
