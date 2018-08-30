# panos_pg

_(versionadded:: 2.3)_


## Synopsis

Create a security profile group


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
<tr><td>commit<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>True</td>
<td></td>
<td><div>commit if changed</div></td></tr>
<tr><td>data_filtering<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>name of the data filtering profile</div></td></tr>
<tr><td>file_blocking<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>name of the file blocking profile</div></td></tr>
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
<tr><td>pg_name<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>name of the security profile group</div></td></tr>
<tr><td>spyware<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>name of the spyware profile</div></td></tr>
<tr><td>url_filtering<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>name of the url filtering profile</div></td></tr>
<tr><td>username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>username for authentication</div></td></tr>
<tr><td>virus<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>name of the anti-virus profile</div></td></tr>
<tr><td>vulnerability<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>name of the vulnerability profile</div></td></tr>
<tr><td>wildfire<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>name of the wildfire analysis profile</div></td></tr>
</table>
</br>



## Examples

    - name: setup security profile group
      panos_pg:
        ip_address: "192.168.1.1"
        password: "admin"
        username: "admin"
        pg_name: "pg-default"
        virus: "default"
        spyware: "default"
        vulnerability: "default"




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

