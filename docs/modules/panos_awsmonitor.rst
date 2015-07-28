.. _panos_awsmonitor:

panos_awsmonitor
``````````````````````````````

Create an AWS monitor object 

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
    <td>access_key</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>access key to use</td>
    </tr>
        <tr>
    <td>monitor_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the vm information source</td>
    </tr>
        <tr>
    <td>secret_access_key</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>secret access key to use</td>
    </tr>
        <tr>
    <td>source</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>EC2 endpoint to monitor (ec2.<region>.amazonaws.com)</td>
    </tr>
        <tr>
    <td>vpc_id</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>ID of the VPC to monitor</td>
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

    
    - name: test
      panos_awsmonitor:
        ip_address: "192.168.1.1"
        password: "admin"
        monitor_name: "awsmonitor"
        vpc_id: "vpc-12345678"
        source: "ec2.eu-west-1.amazonaws.com"
        access_key: "BADACCESSKEY"
        secret_access_key: "BADSECRETACCESSKEY"
