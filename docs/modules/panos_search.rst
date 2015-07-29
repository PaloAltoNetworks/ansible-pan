.. _panos_search:

panos_search
``````````````````````````````

Synopsis
--------

Search and return AMI ID of PA-VM-AWS instance in a specific region.
All the standard EC2 module paramaters are supported.


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
    <td style="vertical-align:middle">release</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      release of PAN-OS<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">first</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">True</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      whether return only the first AMI found<br></td>
    </tr>
        </table><br>


.. important:: Requires pan-python


Examples
--------

 ::

    
    - name: retrieve PA-VM-AWS AMI ID
      panos_search:
        region: "eu-west-1"
        release: "6.1.0"
      register: pavmawsamiid
