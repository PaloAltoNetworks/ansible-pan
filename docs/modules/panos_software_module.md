# panos_software

_(versionadded:: 2.6)_


## Synopsis

Install specific release of PAN-OS.


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
<tr><td>api_key<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>API key to be used instead of <em>username</em> and <em>password</em>.</div></td></tr>
<tr><td>ip_address<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>IP address or hostname of PAN-OS device.</div></td></tr>
<tr><td>password<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Password for authentication for PAN-OS device.  Optional if <em>api_key</em> is used.</div></td></tr>
<tr><td>restart<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Restart device after installing desired version.  Use in conjunction with panos_check to determine when firewall is ready again.</div></td></tr>
<tr><td>username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>Username for authentication for PAN-OS device.  Optional if <em>api_key</em> is used.</div></td></tr>
<tr><td>version<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>Desired PAN-OS release.</div></td></tr>
</table>
</br>



## Examples

    - name: Install PAN-OS 7.1.16 and restart
      panos_software:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        version: '7.1.16'
        restart: true
#### Return Values

The following are the fields unique to this module:

<table border=1 cellpadding=4>
<tr>
<th class="head">name</th>
<th class="head">description</th>
<th class="head">returned</th>
<th class="head">type</th>
<th class="head">sample</th>
</tr>

<tr>
    <td> version </td>
    <td> After performing the software install, returns the version installed on the device. </td>
    <td align=center>  </td>
    <td align=center>  </td>
    <td align=center>  </td>
</tr>

</table>
</br></br>

#### Notes

- Checkmode is not supported.
- Panorama is supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

