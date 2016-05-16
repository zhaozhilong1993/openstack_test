#!/bin/bash
set -x

PATH="/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/opt/dell/srvadmin/bin:/opt/dell/srvadmin/sbin:/root/bin"
fatal () {
    echo -e "\e[1;31m $1...[FAILED]\n\e[0m"
    exit
}

cd /etc/puppet/hieradata/
git status |grep 'modified'
if [[ $? == 0 ]]; then
  fatal "has modify in local-----"
else
  /etc/init.d/httpd stop
  git pull
  sleep 5
  git pull
  /etc/init.d/httpd start
fi
