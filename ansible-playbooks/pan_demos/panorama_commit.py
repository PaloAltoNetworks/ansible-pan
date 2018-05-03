#!/usr/bin/python 

import pandevice
from pandevice import panorama

def commit_panorma():
    "Commit configuration on Panorma to the FW's"

    _panorama = panorama.Panorama('10.8.202.117', 'admin', 'admin')
    _panorama.commit_all(sync=True, sync_all=True, exception=True, devicegroup='cap_one_dg')

if __name__ == "__main__":
    commit_panorma()