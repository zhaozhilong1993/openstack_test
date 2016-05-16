#!/bash/bin

puppet_server=209

usage() {
    echo "usage: $0 <puppet master server >"
    echo
    echo
    echo "example: $0 205"
    exit
}


if [ $# -lt 0 -o $# -gt 2 ]; then
    usage
fi

if [[ $puppet_server == '209' ]]; then

  ssh root@10.255.0.${puppet_server} "ls -lnr /etc/puppet/hieradata/ |awk '{print $9}'"
  region_list=$(ssh root@10.255.0.${puppet_server} "ls -lnr /etc/puppet/hieradata/" |awk '{print $9}'|grep -v Rakefile |grep -v global |grep -v abandon |grep -v '总用量')
  echo "region_list=$region_list"
  for i in $region_list
  do
    env=$(ssh root@10.255.0.${puppet_server} "cat /etc/puppet/hieradata/${i}/common/base.yaml" |grep 'puppet::config::environment'|awk '{print $2}')
    region_id=$(ssh root@10.255.0.${puppet_server} "cat /etc/puppet/hieradata/0.bx.ustack.in/common/base.yaml"  |grep 'sunfire::base::gateway' |awk -F '.' '{print $2}')
    puppet_master_nginx=$(ssh root@10.255.0.33 "sed -n '/\\.${region_id}/N;s/.*\n\(.*\)/\1/p' /etc/nginx/sites-enabled/puppet_host.conf"|awk -F '/' '{print $3}' |awk -F ';' '{print $1}')
    case $puppet_master_nginx in
      "puppet")
        puppet_master=205
        ;;
      "puppet_pre")
        puppet_master=206
        ;;
      "puppet_dev")
        puppet_master=207
        ;;
      "puppet_test")
        puppet_master=208
        ;;
      "puppet_external")
        puppet_master=209
        ;;
      *)
        echo "Unknown puppet_master to known"
        ;;
    esac
    echo "region_name $i 's puppet master=$puppet_master and environment=$env"    
  done
fi
