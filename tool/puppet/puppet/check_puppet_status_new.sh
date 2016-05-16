#!/bin/bash

# write by yuanxiaohua

## use example
# bash check_puppet_status_new.sh lg
##  or
# bash check_puppet_status_new.sh all
## or print log to file
# bash check_puppet_status_new.sh all > puppet.log


############ start ##########
# obtain upgrate date#
echo "`date`"
# update 
  
PATH="/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/opt/dell/srvadmin/bin:/opt/dell/srvadmin/sbin:/root/bin"
dry_run=${dry_run:-false}
exec_ssh_cmd() {
    local host=$1
    shift
    local cmd=$@

    if [ true = "${dry_run}" ]; then
        echo "ssh root@${host} ${cmd}"
    else
        ssh root@${host} ${cmd}
    fi
}
recover_self=${recover_self:-false}
region_name=$1
public_region='uc lg zhsh'
if [[ $region_name == 'all' ]]; then
   private_region_list=`cat /etc/clustershell/groups |grep api |awk -F '_' '{print $1}'|grep -v lg |grep -v zhsh |grep -v uc |grep -v test |grep -v dev`
   public_region='uc lg zhsh'
else
   private_region_list=$region_name
   public_region=$region_name
fi
for i in $public_region; 
    do
      echo "puppet_server=uc 206;region_name=${i}"
      echo "-----disable host ==-----"
      exec_ssh_cmd 10.255.0.206 "mco puppet status -F domain=0.${i}.ustack.in |grep 'disabled;'"
      echo "-----not run puppet host for days ==-----"
      if [ true = "${recover_self}" ]; then
        notrun_puppethosts_uc=$(exec_ssh_cmd 10.255.0.206 "mco puppet status -F domain=0.${i}.ustack.in |grep days |grep -v disabled |awk -F ':' '{print \$1}' |awk -F '-' '{print \$2}'")
        region_id_uc=$(cat /etc/clustershell/groups |grep ^${i}_api |awk -F '.' '{print $2}')
        host_prefix_uc=10.${region_id_uc}.0. 
        for j in $notrun_puppethosts_uc;
            do
              echo "region=${i}--hostname=${j}"
              exec_ssh_cmd ${host_prefix_uc}${j} "for process1 in `ps aux |grep 'puppet agent: applying' |awk '{print $2}'`;do kill -9 $process2;done"
              exec_ssh_cmd ${host_prefix_uc}${j} "rm -f /var/lib/puppet/state/agent_catalog_run.lock;puppet agent -vt"
              sleep 2
        done
      else
        exec_ssh_cmd 10.255.0.206 "mco puppet status -F domain=0.${i}.ustack.in |grep days |grep -v 'disabled;'"

      fi
      
      
done
for k in $private_region_list;
    do
      echo "puppet_server=uc 205;region_name=${k}"
      echo "-----disable host ==-----"
      exec_ssh_cmd 10.255.0.205 "mco puppet status -F domain=0.${k}.ustack.in |grep 'disabled;'"
      echo "-----not run puppet host for days ==-----"
      if [ true = "${recover_self}" ]; then
        notrun_puppethosts_pr=$(exec_ssh_cmd 10.255.0.205 "mco puppet status -F domain=0.${k}.ustack.in |grep days |grep -v disabled |awk -F ':' '{print \$1}' |awk -F '-' '{print \$2}'")
        region_id_pr=$(cat /etc/clustershell/groups |grep ^${k}_api |awk -F '.' '{print $2}')
        host_prefix_pr=10.${region_id_pr}.0. 
        echo "notrun_puppethosts_pr=$notrun_puppethosts_pr-----region_id_pr=$region_id_pr-----host_prefix_pr=$host_prefix_pr"
        for m in $notrun_puppethosts_pr;
            do
              echo "region=${k}--hostname=${m}"
              exec_ssh_cmd ${host_prefix_pr}${m} "for process1 in `ps aux |grep 'puppet agent: applying' |awk '{print $2}'`;do kill -9 $process2;done"
              exec_ssh_cmd ${host_prefix_pr}${m} "rm -f /var/lib/puppet/state/agent_catalog_run.lock;puppet agent -vt"
              sleep 2
        done
      else
        exec_ssh_cmd 10.255.0.205 "mco puppet status -F domain=0.${k}.ustack.in |grep days |grep -v 'disabled;'"

      fi
done
