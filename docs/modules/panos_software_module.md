# panos_software

_(versionadded:: 2.6)_


## Synopsis

Install specific release of PAN-OS.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --------- | -------- | ------- | ------- | -------- |
api_key  |
no |
 |
 |
API key to be used instead of <em>username</em> and <em>password</em>. </td></tr>
ip_address  |
yes |
 |
 |
IP address or hostname of PAN-OS device. </td></tr>
password  |
no |
 |
 |
Password for authentication for PAN-OS device.  Optional if <em>api_key</em> is used. </td></tr>
restart  |
no |
 |
 |
Restart device after installing desired version.  Use in conjunction with panos_check to determine when firewall is ready again. </td></tr>
username  |
no |
admin |
 |
Username for authentication for PAN-OS device.  Optional if <em>api_key</em> is used. </td></tr>
version  |
yes |
 |
 |
Desired PAN-OS release. </td></tr>
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

| name | description | returned | type | sample |

| version | After performing the software install, returns the version installed on the device. |  |  |  </td> |

#### Notes

- Checkmode is not supported.
- Panorama is supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

