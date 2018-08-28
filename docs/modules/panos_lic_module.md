# panos_lic

_(versionadded:: 2.3)_


## Synopsis

Apply an authcode to a device.
The authcode should have been previously registered on the Palo Alto Networks support portal.
The device should have Internet access.


## Requirements (on host that executes module)

- pan-python

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| auth_code  |
| yes |
|  |
| |  |
| authcode to be applied  |
</td></tr>
| force  |
| no |
| false |
| |  |
| whether to apply authcode even if device is already licensed  |
</td></tr>
| ip_address  |
| yes |
|  |
| |  |
| IP address (or hostname) of PAN-OS device  |
</td></tr>
| password  |
| yes |
|  |
| |  |
| password for authentication  |
</td></tr>
| username  |
| no |
| admin |
| |  |
| username for authentication  |
</td></tr>
</table>
</br>



## Examples

        - hosts: localhost
          connection: local
          tasks:
            - name: fetch license
              panos_lic:
                ip_address: "192.168.1.1"
                password: "paloalto"
                auth_code: "IBADCODE"
              register: result
        - name: Display serialnumber (if already registered)
          debug:
            var: "{{result.serialnumber}}"
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| serialnumber | serialnumber of the device in case that it has been already registered | success | string | 973080716 |




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

