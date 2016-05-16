#!/bin/bash
set -x

PATH="/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/opt/dell/srvadmin/bin:/opt/dell/srvadmin/sbin:/root/bin"
fatal () {
    echo -e "\e[1;31m $1...[FAILED]\n\e[0m"
    exit
}

## upgeade sunfire
cd /opt/puppet/devel/sunfire
modify_sunfire=`git status |grep 'modified'`
if [[ $modify_sunfire != 0 ]]; then
  fatal "has modify in sunfire local-----"
else
  /etc/init.d/httpd stop
  git pull
  sleep 5
  git pull
  git checkout master
  git fetch --tags
  tags=`git tag`
  tag=`echo ${tags: -1}`
  git checkout $tag
  git submodule init
  git submodule update
  ln -sd /opt/puppet/pre_production/sunfire/* /etc/puppet/environments/pre_production/modules/
  rm -f /etc/puppet/environments/pre_production/modules/README.md /etc/puppet/environments/pre_production/modules/Release.md
  /etc/init.d/httpd start
fi

