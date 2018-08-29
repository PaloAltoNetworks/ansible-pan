---
title: panos_mgtconfig
---
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
| api_key |  |  |  | API key that can be used instead of <em>username</em>/<em>password</em> credentials. |
| commit |  | True |  | Commit configuration if changed. |
| devicegroup |  |  |  | Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama. |
| dns_server_primary |  |  |  | IP address of primary DNS server. |
| dns_server_secondary |  |  |  | IP address of secondary DNS server. |
| domain |  |  |  | The domain of the device |
| hostname |  |  |  | The hostname of the device. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| login_banner |  |  |  | Login banner text. |
| ntp_server_primary |  |  |  | IP address (or hostname) of primary NTP server. |
| ntp_server_secondary |  |  |  | IP address (or hostname) of secondary NTP server. |
| panorama_primary |  |  |  | IP address (or hostname) of primary Panorama server. |
| panorama_secondary |  |  |  | IP address (or hostname) of secondary Panorama server. |
| password | yes |  |  | Password credentials to use for auth unless <em>api_key</em> is set. |
| timezone |  |  |  | Device timezone. |
| update_server |  |  |  | IP or hostname of the update server. |
| username |  | admin |  | Username credentials to use for auth unless <em>api_key</em> is set. |

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

