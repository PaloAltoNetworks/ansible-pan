.. _panos_content:

panos_content
``````````````````````````````

Synopsis
--------

Upgrade PAN-OS device dynamic updates with the latest available version

Options
-------

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">username</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">admin</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      username for authentication<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">wildfire_update</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      whether Wildfire signatures should be updated<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">url_download_region</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      region to download PAN-DB seed for<br>if null, PAN-DB won't be updated<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">content_update</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      whether content (Apps or Apps+Threats) should be updated<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">password</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      password for authentication<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">ip_address</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      IP address (or hostname) of PAN-OS device<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">job_timeout</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">240</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      timeout for download and install jobs in seconds<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">anti_virus_update</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      whether Anti-Virus signatures should be updated<br></td>
    </tr>
        </table><br>


.. important:: Requires pan-python


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
