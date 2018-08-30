# panos_admin

_(versionadded:: 2.3)_


## Synopsis

PanOS module that allows changes to the user account passwords by doing API calls to the Firewall using pan-api as the protocol.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python

## Options

<table border=1 cellpadding=4>
<tr>
<th class="head">parameter</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>
<tr><td>admin_password<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>New password for <em>admin_username</em> user</div></td></tr>
<tr><td>admin_username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>Username that needs password change.</div></td></tr>
<tr><td>api_key<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>API key that can be used instead of <em>username</em>/<em>password</em> credentials.</div></td></tr>
<tr><td>commit<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>True</td>
<td></td>
<td><div>Commit configuration if changed.</div></td></tr>
<tr><td>ip_address<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>IP address (or hostname) of PAN-OS device being configured.</div></td></tr>
<tr><td>password<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>Password credentials to use for auth unless <em>api_key</em> is set.</div></td></tr>
<tr><td>role<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>role for admin user</div></td></tr>
<tr><td>username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>Username credentials to use for auth unless <em>api_key</em> is set.</div></td></tr>
</table>
</br>



## Examples

    # Set the password of user admin to "badpassword"
    # Doesn't commit the candidate config
      - name: set admin password
        panos_admin:
          ip_address: "192.168.1.1"
          password: "admin"
          admin_username: admin
          admin_password: "badpassword"
          commit: False
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



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

