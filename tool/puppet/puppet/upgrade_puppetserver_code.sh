#!/bin/bash

puppet_server=$1
code=$2

usage() {
    echo "usage: $0 <puppet master server > <module name>"
    echo
    echo
    echo "example: $0 205 hieradata"
    exit
}


if [ $# -lt 1 -o $# -gt 2 ]; then
    usage
fi

if [[ $puppet_server == '205' ]]; then
  case $code in
    "hieradata")
      ssh root@10.255.0.${puppet_server} "curl http://10.255.0.205:8888/puppet/upgrade_hieradata.sh |bash"
      ;;
    "sunfire")
      ssh root@10.255.0.${puppet_server} "curl http://10.255.0.205:8888/puppet/upgrade_puppetmodule_sunfire.sh |bash"
      ;;
    "storm")
      ssh root@10.255.0.${puppet_server} "curl http://10.255.0.205:8888/puppet/upgrade_puppetmodule_storm.sh |bash"
      ;;
    "karma")
      ssh root@10.255.0.${puppet_server} "curl http://10.255.0.205:8888/puppet/upgrade_puppetmodule_karma.sh |bash"
      ;;
    *)
      echo "Unknown code to upgrade"
      ;;
   esac
elif [[ $puppet_server == '206' ]];then
  case $code in
    "hieradata")
      ssh root@10.255.0.${puppet_server} "curl http://10.255.0.205:8888/puppet/upgrade_hieradata.sh |bash"
      ;;
    "sunfire")
      ssh root@10.255.0.${puppet_server} "curl http://10.255.0.205:8888/puppet/upgrade_puppetmodule_sunfire.sh |bash"
      ;;
    "storm")
      ssh root@10.255.0.${puppet_server} "curl http://10.255.0.205:8888/puppet/upgrade_puppetmodule_storm.sh |bash"
      ;;
    "karma")
      ssh root@10.255.0.${puppet_server} "curl http://10.255.0.205:8888/puppet/upgrade_puppetmodule_karma.sh |bash"
      ;;
    *)
      echo "Unknown code to upgrade"
      ;;
   esac
elif [[ $puppet_server == '208' ]];then
  case $code in
    "hieradata")
      ssh root@10.255.0.${puppet_server} "curl http://10.255.0.205:8888/puppet/upgrade_hieradata.sh |bash"
      ;;
    "sunfire")
      ssh root@10.255.0.${puppet_server} "curl http://10.255.0.205:8888/puppet/upgrade_puppetmodule_sunfire.sh |bash"
      ;;
    "storm")
      ssh root@10.255.0.${puppet_server} "curl http://10.255.0.205:8888/puppet/upgrade_puppetmodule_storm.sh |bash"
      ;;
    "karma")
      ssh root@10.255.0.${puppet_server} "curl http://10.255.0.205:8888/puppet/upgrade_puppetmodule_karma.sh |bash"
      ;;
    *)
      echo "Unknown code to upgrade"
      ;;
   esac
fi
