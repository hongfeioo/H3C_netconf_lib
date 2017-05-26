# ¿¿

1. ¿¿manager.py¿¿¿¿¿¿¿¿
```
 host = '172.16.1.162' #¿¿¿¿¿¿ 
 user = 'aaa' #netconf¿¿¿ 
 password = 'aaa' #netconf¿¿

¿¿¿¿¿¿h3c¿¿¿¿netconf¿¿ ¿¿,¿h3c¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿press¿¿¿
system-view 
local-user aaa class manage 
password simple aaa 
authorization-attribute user-role network-admin work-directory flash:/ 
service-type https 
quit 
netconf soap https enable 
quit
```

2. ¿¿set_static_route_table¿¿¿¿¿¿¿ ¿¿delete_static_route_table.py¿¿¿¿¿¿¿

¿¿¿¿¿¿¿¿¿manager.py¿¿¿netconf¿¿¿¿ doc/Comware V7 StaticRoute NETCONF XML API Configuration Reference
```
¿¿¿¿¿¿¿¿¿¿¿¿ 
DestVrfIndex = '0' 
DestTopologyIndex = '0' 
Ipv4Address = '3.3.3.3' 
Ipv4PrefixLength = '24' 
NexthopVrfIndex = '0' 
NexthopIpv4Address = '4.4.4.1' 
IfIndex = '0'
```

3. ¿¿¿¿¿H3C¿¿¿¿¿
