.. _panos_cstapphost:

panos_cstapphost
``````````````````````````````

Create a custom application for internal website based on the Host header 

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
    <td>convert_hostname</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>wheter convert string given as regex in a real regex</td>
    </tr>
        <tr>
    <td>app_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the new custom application</td>
    </tr>
        <tr>
    <td>host_regex</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>regex to match against the Host header</td>
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
        </table>

Examples
--------

 ::

    
    # create a custom application for traffic for test.example.com
    - name: setup custom application
      panos_cstapphost:
        ip_address: "192.168.1.1"
        password: "admin"
        username: "admin"
        app_name: "test"
        host_regex: "test\.example\.com"
