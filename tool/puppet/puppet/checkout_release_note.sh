#!/bin/bash


old_tag=$1
new_tag=$2

warn () {
    echo -e "\e[1;31m $1...[WARN]\n\e[0m"
}

usage() {
    echo "usage: $0 <old_tag> [new_tag]"
    echo
    echo
    echo "example: $0 0.8.3 0.8.6"
    exit
}


if [ $# -lt 1 -o $# -gt 2 ]; then
    usage
fi

## checkout commit BF ##
echo -e "\e[1;34m commit is BF===\n\e[0m"
git log "${old_tag}".."${new_tag}" --oneline |grep BF

## checkout commit NF ##
echo -e "\e[1;34m commit is NF===\n\e[0m"
git log "${old_tag}".."${new_tag}" --oneline |grep NF

## checkout commit RF ##
echo -e "\e[1;34m commit is RF===\n\e[0m"
git log "${old_tag}".."${new_tag}" --oneline |grep RF

## checkout commit log contain criticality hight
echo -e "\e[1;34m checkout commit log contain Criticality high===\n\e[0m"
git log "${old_tag}".."${new_tag}" |grep -i Criticality |grep -i high > /dev/null &&  is_criticality=1 && warn 'This release contain  High criticality!'
if [[ $is_criticality == 1 ]];then
  commit_list=`git log ${old_tag}..${new_tag} |grep commit |awk '{print $2'}`
  for i in $commit_list
  do
      criticality_high=`git show $i |grep -i Criticality |grep -i high`
      if [[ -z $criticality_high ]]; then
        continue
      else
        echo "contain Criticality high commit is $i"
      fi
  done
fi

## checkout commit log contain  Mandatory Hieradata
echo -e "\e[1;34m checkout commit log contain Mandatory Hieradata===\n\e[0m"
git log "${old_tag}".."${new_tag}" |grep -i Hieradata| grep -iE 'Yes|Mandatory' > /dev/null &&  is_Mandatory_Hieradata=1 && warn 'This release contain  Mandatory Hieradata!'
if [[ $is_Mandatory_Hieradata == 1 ]];then
  commit_list=`git log ${old_tag}..${new_tag} |grep commit |awk '{print $2'}`
  for i in $commit_list
  do
      Mandatory_Hieradata=`git show $i |grep -i Hieradata| grep -iE 'Yes|Mandatory'`
      if [[ -z $Mandatory_Hieradata ]]; then
        continue
      else
        echo "contain Mandatory Hieradata commit is $i"
      fi
  done
fi

## checkout commit log contain  Forward compatibility
echo -e "\e[1;34m checkout commit log contain Forward compatibility is no===\n\e[0m"
git log "${old_tag}".."${new_tag}" |grep -i 'Forward compatibility'|grep -i 'no' > /dev/null &&  is_noForward_compatibility=1 && warn 'This release contain Forward compatibility is no!'
if [[ $is_noForward_compatibility == 1 ]];then
  commit_list=`git log ${old_tag}..${new_tag} |grep commit |awk '{print $2'}`
  for i in $commit_list
  do
      Forward_compatibility_no=`git show $i |grep -i 'Forward compatibility'|grep -i 'no'`
      if [[ -z $Forward_compatibility_no ]]; then
        continue
      else
        echo "contain Forward compatibility is no commit is $i"
      fi
  done
fi
