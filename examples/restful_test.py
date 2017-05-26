# -*- coding:utf-8 -*-
from lib import restclient
import json

host = '172.16.1.162'
user = 'aaa'
password = 'aaa'

rest = restclient.RESTFUL(host, user, password)


def get_vlan_name(vlan_id):
    resp_j = rest.get('VLAN/VLANs?index=ID=%d' % vlan_id)
    if resp_j:
        resp = json.loads(resp_j)
        print resp.get('Name')


if __name__ == '__main__':
    get_vlan_name(1)
