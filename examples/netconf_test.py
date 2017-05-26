from lib import netconf

host = '172.16.1.162'
user = 'aaa'
password = 'aaa'


vlan_xml = """
<VLAN>
  <VLANs>
    <VLANID>
      <ID></ID>
      <Description></Description>
      <Name></Name>
      <AccessPortList></AccessPortList>
      <Ipv4>
        <Ipv4Address></Ipv4Address>
        <Ipv4Mask></Ipv4Mask>
      </Ipv4>
    </VLANID>
  </VLANs>
</VLAN>
"""

netconf_client = netconf.NETCONF(host, user, password)


def get_vlan_name(vlan_id):
    if netconf_client is not None:
        resp = netconf_client.get_bulk(vlan_xml, str(vlan_id), 'Name')
        print resp['Name'][0]

if __name__ == '__main__':
    get_vlan_name(1)