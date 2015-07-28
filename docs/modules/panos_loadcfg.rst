.. _panos_loadcfg:

panos_loadcfg
``````````````````````````````

Load configuration on PAN-OS device 

.. raw:: html

    <table>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
        <tr>
    <td>username</td>
    <td>no</td>
    <td>admin</td>
    <td><ul></ul></td>
    <td>username for authentication</td>
    </tr>
        <tr>
    <td>commit</td>
    <td>no</td>
    <td>True</td>
    <td><ul></ul></td>
    <td>commit if changed</td>
    </tr>
        <tr>
    <td>password</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>password for authentication</td>
    </tr>
        <tr>
    <td>ip_address</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>IP address (or hostname) of PAN-OS device</td>
    </tr>
        <tr>
    <td>file</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>configuration file to load</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # Import and load config file from URL
      - name: import configuration
        panos_import:
          ip_address: "192.168.1.1"
          password: "admin"
          url: "{{ConfigURL}}"
          category: "configuration"
        register: result
      - name: load configuration
        panos_loadcfg:
          ip_address: "192.168.1.1"
          password: "{{password}}"
          file: "{{result.filename}}"
