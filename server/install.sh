#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

cd "$(
    cd "$(dirname "$0")" || exit
    pwd
)" || exit

#fonts color
Green="\033[32m"
Red="\033[31m"
# Yellow="\033[33m"
GreenBG="\033[42;37m"
RedBG="\033[41;37m"
Font="\033[0m"

#notification information
# Info="${Green}[信息]${Font}"
OK="${Green}[OK]${Font}"
Error="${Red}[错误]${Font}"

infoFile="/var/countra/data/sysinfos"
choice=0

alias cp="cp"

read -rp "是否安装python38: " python_install
    [[ -z ${python_install} ]] && python_install="Y"
    case $python_install in
    [yY][eE][sS] | [yY])
        echo -e "${GreenBG} 安装python38 ${Font}"
        wget https://raw.githubusercontent.com/Countra/scripts/master/python/install_py38.sh
        chmod +x install_py38.sh
        bash install_py38.sh
        echo -e "${GreenBG} 配置完成 ${Font}"
        ;;
    *)
        echo -e "${RedBG} 跳过安装python38 ${Font}"
        ;;
    esac

read -rp "是否替换ssh登录前提示信息" info_head
    [[ -z ${info_head} ]] && info_head="Y"
    case $info_head in
    [yY][eE][sS] | [yY])
        echo "Banner /etc/issue.net" >> /etc/ssh/sshd_config
        cp ./issue.net /etc/issue.net
        echo -e "${GreenBG} 替换完成 ${Font}"
        ;;
    *)
        echo -e "${RedBG} 跳过 ${Font}"
        ;;
    esac

read -rp "是否设置ssh登录显示信息 " info_in
    [[ -z ${info_in} ]] && info_in="Y"
    case $info_in in
    [yY][eE][sS] | [yY])
        choice=0
        ;;
    *)
        choice=1
        ;;
    esac

if [[ "${choice}" == 0 ]];then
        read -rp "是否覆盖之前的登录显示信息 " info_ini
            [[ -z ${info_ini} ]] && info_ini="Y"
            case $info_ini in
            [yY][eE][sS] | [yY])
                echo "" > /etc/motd
                rm -rf /etc/motd.d/*
                cp ./countra /etc/motd.d/
                mkdir -p /var/countra/
                mkdir -p /var/countra/data/
                cp ./infoMotd.py /var/countra/
                echo "alias cp=\"cp\"" >> /etc/profile
                echo "python38 /var/countra/infoMotd.py" >> /etc/profile
                echo "cp /var/countra/data/sysinfos /etc/motd.d/" >> /etc/profile
                echo -e "${GreenBG} 完成 ${Font}"
                ;;
            *)
                cp ./countra /etc/motd.d/
                mkdir -p /var/countra/
                mkdir -p /var/countra/data/
                cp ./infoMotd.py /var/countra/
                echo "alias cp=\"cp\"" >> /etc/profile
                echo "python38 /var/countra/infoMotd.py" >> /etc/profile
                echo "cp /var/countra/data/sysinfos /etc/motd.d/" >> /etc/profile
                echo -e "${GreenBG} 完成 ${Font}"
                ;;
            esac
    else
        echo -e "${Error} ${RedBG} 跳过 ${Font}"
    fi

service sshd restart

echo -e "\n"
read -s -n1 -p "按任意键返回菜单 ... "