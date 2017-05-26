from lib import netconf

host = '172.16.1.167'
user = 'aaa'
password = 'aaa'


StaticRoute_xml_merge_body = """
<StaticRoute xc:operation="merge">
   <Ipv4StaticRouteConfigurations>
      <RouteEntry>
         <DestVrfIndex>%s</DestVrfIndex>
         <DestTopologyIndex>%s</DestTopologyIndex>
         <Ipv4Address>%s</Ipv4Address>
         <Ipv4PrefixLength>%s</Ipv4PrefixLength>
         <NexthopVrfIndex>%s</NexthopVrfIndex>
         <NexthopIpv4Address>%s</NexthopIpv4Address>
         <IfIndex>%s</IfIndex>
      </RouteEntry>
   </Ipv4StaticRouteConfigurations>
</StaticRoute>
"""

StaticRoute_xml_delete_body = """
<StaticRoute xc:operation="delete">
   <Ipv4StaticRouteConfigurations>
      <RouteEntry>
         <DestVrfIndex>%s</DestVrfIndex>
         <DestTopologyIndex>%s</DestTopologyIndex>
         <Ipv4Address>%s</Ipv4Address>
         <Ipv4PrefixLength>%s</Ipv4PrefixLength>
         <NexthopVrfIndex>%s</NexthopVrfIndex>
         <NexthopIpv4Address>%s</NexthopIpv4Address>
         <IfIndex>%s</IfIndex>
      </RouteEntry>
   </Ipv4StaticRouteConfigurations>
</StaticRoute>
"""

DestVrfIndex = '0'
DestTopologyIndex = '0'
Ipv4Address = '3.3.3.3'
Ipv4PrefixLength = '24'
NexthopVrfIndex = '0'
NexthopIpv4Address = '4.4.4.1'
IfIndex = '0'


def set_static_route_table():
    netconf_client = netconf.NETCONF(host, user, password)
    if netconf_client is not None:
        resp = netconf_client.Set(StaticRoute_xml_merge_body %
                                  (DestVrfIndex,
                                   DestTopologyIndex,
                                   Ipv4Address,
                                   Ipv4PrefixLength,
                                   NexthopVrfIndex,
                                   NexthopIpv4Address,
                                   IfIndex))
        netconf_client.close_session()


def delete_static_route_table():
    netconf_client = netconf.NETCONF(host, user, password)
    if netconf_client is not None:
        resp = netconf_client.Set(StaticRoute_xml_delete_body %
                                  (DestVrfIndex,
                                   DestTopologyIndex,
                                   Ipv4Address,
                                   Ipv4PrefixLength,
                                   NexthopVrfIndex,
                                   NexthopIpv4Address,
                                   IfIndex))
        netconf_client.close_session()
