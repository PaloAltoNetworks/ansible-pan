# panos_mgtconfig

_(versionadded:: 2.4)_


## Synopsis

Configure management settings of device. Not all configuration options are configurable at this time.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key  |
| no |
|  |
| |  |
| API key that can be used instead of <em>username</em>/<em>password</em> credentials.  |
</td></tr>
| commit  |
| no |
| True |
| |  |
| Commit configuration if changed.  |
</td></tr>
| devicegroup  |
| no |
|  |
| |  |
| Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama.  |
</td></tr>
| dns_server_primary  |
| no |
|  |
| |  |
| IP address of primary DNS server.  |
</td></tr>
| dns_server_secondary  |
| no |
|  |
| |  |
| IP address of secondary DNS server.  |
</td></tr>
| domain  |
| no |
|  |
| |  |
| The domain of the device  |
</td></tr>
| hostname  |
| no |
|  |
| |  |
| The hostname of the device.  |
</td></tr>
| ip_address  |
| yes |
|  |
| |  |
| IP address (or hostname) of PAN-OS device being configured.  |
</td></tr>
| login_banner  |
| no |
|  |
| |  |
| Login banner text.  |
</td></tr>
| ntp_server_primary  |
| no |
|  |
| |  |
| IP address (or hostname) of primary NTP server.  |
</td></tr>
| ntp_server_secondary  |
| no |
|  |
| |  |
| IP address (or hostname) of secondary NTP server.  |
</td></tr>
| panorama_primary  |
| no |
|  |
| |  |
| IP address (or hostname) of primary Panorama server.  |
</td></tr>
| panorama_secondary  |
| no |
|  |
| |  |
| IP address (or hostname) of secondary Panorama server.  |
</td></tr>
| password  |
| yes |
|  |
| |  |
| Password credentials to use for auth unless <em>api_key</em> is set.  |
</td></tr>
| timezone  |
| no |
|  |
| |  |
| Device timezone.  |
</td></tr>
| update_server  |
| no |
|  |
| |  |
| IP or hostname of the update server.  |
</td></tr>
| username  |
| no |
| admin |
| |  |
| Username credentials to use for auth unless <em>api_key</em> is set.  |
</td></tr>
</table>
</br>



## Examples

    - name: set dns and panorama
      panos_mgtconfig:
        ip_address: "192.168.1.1"
        password: "admin"
        dns_server_primary: "1.1.1.1"
        dns_server_secondary: "1.1.1.2"
        panorama_primary: "1.1.1.3"
        panorama_secondary: "1.1.1.4"
        ntp_server_primary: "1.1.1.5"
        ntp_server_secondary: "1.1.1.6"

#### Notes

- Checkmode is not supported.
- Panorama is supported



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

