# panos_restart

_(versionadded:: 2.3)_


## Synopsis

Restart a device either through Panorama or going directly to a firewall.


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
<td><div>API key that can be used instead of <em>username</em>/<em>password</em> credentials.</div></td></tr>
<tr><td>devicegroup<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama.</div><div>If device group is not define we assume that we are contacting Firewall.</div></td></tr>
<tr><td>ip_address<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>IP address (or hostname) of PAN-OS device being configured.</div></td></tr>
<tr><td>password<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Password credentials to use for auth unless <em>api_key</em> is set.</div></td></tr>
<tr><td>username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>Username credentials to use for auth unless <em>api_key</em> is set.</div></td></tr>
</table>
</br>



## Examples

    - panos_restart:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
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
    <td> status </td>
    <td> success status </td>
    <td align=center> success </td>
    <td align=center> string </td>
    <td align=center> okey dokey </td>
</tr>

</table>
</br></br>

#### Notes

- Checkmode is not supported.
- Panorama is supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

