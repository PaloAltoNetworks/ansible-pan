# panos_interface

_(versionadded:: 2.3)_


## Synopsis

Configure data-port (DP) network interface for DHCP. By default DP interfaces are static.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

<table border=1 cellpadding=4>
<tr>
<th class="head">parameter</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>
<tr><td>adjust_tcp_mss<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Adjust TCP MSS for layer3 interface.</div></td></tr>
<tr><td>aggregate_group<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Aggregate interface name.</div></td></tr>
<tr><td>api_key<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>API key that can be used instead of <em>username</em>/<em>password</em> credentials.</div></td></tr>
<tr><td>comment<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Interface comment.</div></td></tr>
<tr><td>commit<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>True</td>
<td></td>
<td><div>Commit if changed</div></td></tr>
<tr><td>create_default_route<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>false</td>
<td></td>
<td><div>Whether or not to add default route with router learned via DHCP.</div></td></tr>
<tr><td>dhcp_default_route_metric<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Metric for the DHCP default route.</div></td></tr>
<tr><td>enable_dhcp<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>true</td>
<td></td>
<td><div>Enable DHCP on this interface.</div></td></tr>
<tr><td>if_name<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>Name of the interface to configure.</div></td></tr>
<tr><td>ip<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>List of static IP addresses.</div></td></tr>
<tr><td>ip_address<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>IP address (or hostname) of PAN-OS device being configured.</div></td></tr>
<tr><td>ipv4_mss_adjust<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>(7.1+) TCP MSS adjustment for IPv4.</div></td></tr>
<tr><td>ipv6_enabled<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Enable IPv6.</div></td></tr>
<tr><td>ipv6_mss_adjust<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>(7.1+) TCP MSS adjustment for IPv6.</div></td></tr>
<tr><td>link_duplex<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Link duplex.  Supported values are <em>auto</em>/<em>full</em>/<em>half</em>.</div></td></tr>
<tr><td>link_speed<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Link speed.  Supported values are <em>auto</em>/<em>10</em>/<em>100</em>/<em>1000</em>.</div></td></tr>
<tr><td>link_state<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Link state.  Supported values are <em>auto</em>/<em>up</em>/<em>down</em>.</div></td></tr>
<tr><td>lldp_enabled<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Enable LLDP for layer2 interface.</div></td></tr>
<tr><td>lldp_profile<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>LLDP profile name for layer2 interface.</div></td></tr>
<tr><td>management_profile<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Interface management profile name.</div></td></tr>
<tr><td>mode<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>layer3</td>
<td></td>
<td><div>The interface mode.</div><div>Supported values are <em>layer3</em>/<em>layer2</em>/<em>virtual-wire</em>/<em>tap</em>/<em>ha</em>/<em>decrypt-mirror</em>/<em>aggregate-group</em></div></td></tr>
<tr><td>mtu<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>MTU for layer3 interface.</div></td></tr>
<tr><td>netflow_profile<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Netflow profile for layer3 interface.</div></td></tr>
<tr><td>netflow_profile_l2<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Netflow profile name for layer2 interface.</div></td></tr>
<tr><td>operation<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>add</td>
<td></td>
<td><div>The action to be taken.  Supported values are <em>add</em>/<em>update</em>/<em>delete</em>.</div></td></tr>
<tr><td>password<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Password credentials to use for auth.</div></td></tr>
<tr><td>username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>Username credentials to use for auth.</div></td></tr>
<tr><td>vr_name<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>default</td>
<td></td>
<td><div>Name of the virtual router; it must already exist.</div></td></tr>
<tr><td>vsys_dg<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>vsys1</td>
<td></td>
<td><div>Name of the vsys (if firewall) or device group (if panorama) to put this object.</div></td></tr>
<tr><td>zone_name<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>Name of the zone for the interface. If the zone does not exist it is created.</div><div>If the zone exists and it is not of the correct mode the operation will fail.</div></td></tr>
</table>
</br>



## Examples

    # Create ethernet1/1 as DHCP.
    - name: enable DHCP client on ethernet1/1 in zone public
      panos_interface:
        ip_address: "192.168.1.1"
        username: "ansible"
        password: "secret"
        if_name: "ethernet1/1"
        zone_name: "public"
        create_default_route: "yes"
    
    # Update ethernet1/2 with a static IP address in zone dmz.
    - name: ethernet1/2 as static in zone dmz
      panos_interface:
        ip_address: "192.168.1.1"
        username: "ansible"
        password: "secret"
        if_name: "ethernet1/2"
        mode: "layer3"
        ip: ["10.1.1.1/24"]
        enable_dhcp: false
        zone_name: "dmz"




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

