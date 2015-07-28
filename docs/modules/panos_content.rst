.. _panos_content:

panos_content
``````````````````````````````

Upgrade PAN-OS device dynamic updates with the latest available version 

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
    <td>wildfire_update</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>whether Wildfire signatures should be updated</td>
    </tr>
        <tr>
    <td>url_download_region</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>region to download PAN-DB seed forif null, PAN-DB won't be updated</td>
    </tr>
        <tr>
    <td>content_update</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>whether content (Apps or Apps+Threats) should be updated</td>
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
    <td>job_timeout</td>
    <td>no</td>
    <td>240</td>
    <td><ul></ul></td>
    <td>timeout for download and install jobs in seconds</td>
    </tr>
        <tr>
    <td>anti_virus_update</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>whether Anti-Virus signatures should be updated</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # upgrade content to the lastest release
    - name: upgrade content
      panos_content:
        ip_address: "192.168.1.1"
        password: "admin"
        content_update: yes
    
    # upgrade anti-virus and wildfire signatures to the
    # latest releases
    - name: upgrade anti-virus
      panos_content:
        ip_address: "192.168.1.1"
        password: "admin"
        anti_virus_update: yes
        wildfire_update: yes
    
    # download PAN-DB seed for Europe region
    - name: upgrade pan-db
      panos_content:
        ip_address: "{{stack.stack_outputs.PAVMAWSEIPMgmt}}"
        password: "{{admin_password}}"
        url_download_region: europe
