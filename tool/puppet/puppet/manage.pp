define manage(
  $iface = $name,
  $type,
  $network_prefix,
  $ipaddr,
  $netmask,
  $macaddr,
  $gateway,
){
  if has_interface_with($iface) {
    if $netmask {
      $real_netmask  = $netmask
    } else {
      $real_netmask  = getvar("::netmask_${iface}")
    }
    if $macaddr {
      $real_macaddr  = $macaddr
    } else {
      $real_macaddr  = getvar("::macaddress_${iface}")
    }
    # Set ip automatically
    if $iface['ipaddr'] == 'UNSET' {
      $hostname_array=split($::hostname,'-')
      # make sure hostname is xxx-000 format
      validate_array($hostname_array)
      $ip_suffix=$hostname_array[1]
      $real_ip = "${network_prefix}${ip_suffix}"
    } else {
      $real_ip = $ipaddr
   }
    network::if::static { $iface:
      ensure     => 'up',
      ipaddress  => $real__ip,
      netmask    => $real_netmask,
      macaddress => $real_macaddr,
      gateway    => $gateway,
    }
  }
}

