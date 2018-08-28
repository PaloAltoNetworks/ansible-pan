# panos_check

_(versionadded:: 2.3)_


## Synopsis

Check if PAN-OS device is ready for being configured (no pending jobs).
The check could be done once or multiple times until the device is ready.


## Requirements (on host that executes module)

- pan-python

## Options

<table border=1 cellpadding=4>
<tr>
<th class="head">parameter</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>
<tr><td>interval<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>0</td>
<td></td>
<td><div>time waited between checks</div></td></tr>
<tr><td>ip_address<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>IP address (or hostname) of PAN-OS device</div></td></tr>
<tr><td>password<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>password for authentication</div></td></tr>
<tr><td>timeout<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>0</td>
<td></td>
<td><div>timeout of API calls</div></td></tr>
<tr><td>username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>username for authentication</div></td></tr>
</table>
</br>



## Examples

    # single check on 192.168.1.1 with credentials admin/admin
    - name: check if ready
      panos_check:
        ip_address: "192.168.1.1"
        password: "admin"
    
    # check for 10 times, every 30 seconds, if device 192.168.1.1
    # is ready, using credentials admin/admin
    - name: wait for reboot
      panos_check:
        ip_address: "192.168.1.1"
        password: "admin"
      register: result
      until: not result|failed
      retries: 10
      delay: 30




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

