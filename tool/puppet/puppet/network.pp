# == Class: network
#
# Full description of class network here.
#
# === Parameters
#
# Document parameters here.
#
# [*sample_parameter*]
#   Explanation of what this parameter affects and what it defaults to.
#   e.g. "Specify one or more upstream ntp servers as an array."
#
# === Variables
#
# Here you should define a list of variables that this module would require.
#
# [*sample_variable*]
#   Explanation of how this variable affects the funtion of this class and if
#   it has a default. e.g. "The parameter enc_ntp_servers must be set by the
#   External Node Classifier as a comma separated list of hostnames." (Note,
#   global variables should be avoided in favor of class parameters as
#   of Puppet 2.6.)
#
# === Examples
#
#  class { 'network':
#    servers => [ 'pool.ntp.org', 'ntp.local.company.com' ],
#  }
#
# === Authors
#
# Author Name <author@domain.com>
#
# === Copyright
#
# Copyright 2015 Your name here, unless otherwise noted.
#
class network (
  $iface_list,
  $bond_list,
  $bridge_list,
  $ovs_bridge_list,
){
  if $iface_list {
    validate_array($iface_list)
  }
  if $bond_list {
    validate_array($bond_list)
  }
  if $bridge_list {
    validate_array($bridge_list)
  }
  if $ovs_bridge_list {
    validate_array($ovs_bridge_list)
  }

  $iface_list.each | $iface | {
    if $iface['type'] == 'dummy' {
      network::if::dummy { $iface['name']:
         ensure => 'up',
      }
    }
    # Static type
    elsif $iface['type'] == 'static' {
      # Management network auto configuration
      if $iface['nettype'] == 'management'{
        # Set ip on eth0 automatically
      }
      # Network type is not management
      else {
        network::if::static { $iface['name']:
          ensure     => 'up',
          ipaddress  => $iface['ipaddr'],
          netmask    => $iface['netmask'],
          macaddress => $iface['macaddr'],
          gateway    => $iface['gateway'],
        }
      }
      # Configure route
      if $iface['route'] {
        file {"/etc/sysconfig/network-scripts/route-$iface['name']":
          ensure  => present,
          owner   => 'root',
          mode    => '0644',
          content => template('sunfire/route-eth.erb')
        }
      }
    }
    # Invalid tpye
    else {
      fail('Invalid interface type.')
    }
  }

  $bond_list.each | $bond | {
    if $bond['type'] == 'dummy' {
      network::bond::dummy { $bond['name']:
        ensure => 'up',
      }
    }
    elsif $bond['type'] == 'static' {
      # IP confiuration
      if $bond['nettype']  == 'management' {
        sunfire::mangement { $bond['name']:
          #...
        }
      }
      else {
        network::bond::static { $bond['name']:
          ensure       => 'up',
          ipaddress    => $bond['ipaddr'],
          netmask      => $bond['netmask'],
          gateway      => $bond['gateway'],
          mtu          => $bond['mtu'],
          bonding_opts => 'mode=4 miimon=100',
        }
      }
      # Route confiuration
      if $iface['route'] {
        file {"/etc/sysconfig/network-scripts/route-$bond['name']":
          ensure  => present,
          owner   => 'root',
          mode    => '0644',
          content => template('sunfire/route-eth.erb')
        }
      }
    }
    else {
      fail('Invalid bond type.')
    }
    # Children confiuration
    $bond['children'].each | $child | {
      network::bond::slave { $child :
        master     => $bond['name'],
        macaddress => getvar("::macaddress_${child}"),
      }
    }
  }

  $bridge_list.each | $bri | {
    if $bri['type'] == 'dummy' {
      network::bridge::dummy { $bri['name']:
        ensure => 'up',
      }
    }
    elsif $bri['type'] == 'static' {
      network::bridge::static { $bri['name']:
        ensure       => 'up',
        ipaddress    => $bri['ipaddr'],
        netmask      => $bri['netmask'],
        gateway      => $bri['gateway'],
      }
    }
    # Children confiuration
    $bri['children'].each | $child | {
      if $child['type'] == 'bond' {
        network::bond::bridge { $child:
          ensure       => 'up',
          bridge       => $bri['name'],
          mtu          => $child['mtu'],
          bonding_opts => 'mode=4 miimon=100',
        }
      }
      elsif $child['type'] == 'normal' {
        network::if::bridge { $child:
          ensure       => 'up',
          bridge       => $bri['name'],
          mtu          => $child['mtu'],
         }
      }
      elsif $child['type'] == 'vlan' {
        network::if::vlan { $child:
          ensure       => 'up',
          bridge       => $bri,
          mtu          => $child['mtu'],
        }
      }
    }
  }


  $ovs_bridge_list.each | $ovs | {
    if $ovs['type'] == 'dummy' {
      network::ovs::dummy { $ovs['name']:
        ensure => 'up',
      }
    }
    elsif $ovs'type'] == 'static' {
      network::ovs::static { $ovs['name']:
        ensure       => 'up',
        ipaddress    => $ovs['ipaddr'],
        netmask      => $ovs['netmask'],
        gateway      => $ovs['gateway'],
        domain       => $ovs['domain'],
      }
    }
    # Children confiuration
    $ovs['children'].each | $child | {
      if $child['type'] == 'bond' {
        network::bond::ovs { $child:
          ensure       => 'up',
          bridge       => $ovs['name'],
          mtu          => $child['mtu'],
        }
      }
      elsif $child['type'] == 'normal' {
        network::if::ovs { $child:
          ensure       => 'up',
          bridge       => $ovs['name'],
          mtu          => $child['mtu'],
         }
      }
      elsif $child['ctype'] == 'vlan' {
        network::if::vlan { $child:
          ensure       => 'up',
          bridge       => $ovs['name'],
          mtu          => $child['mtu'],
        }
      }
    }
  }
}
