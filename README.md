# 简介

1. 请在manager.py里面填如下信息： 
```
host = '172.16.1.162' #要登录的主机 
user = 'aaa' #netconf用户名 
password = 'aaa' #netconf密码

注意：请保证h3c设备开启netconf服务 例如,在h3c交换机上配置如下信息，具体参见press手册。 
system-view 
local-user aaa class manage 
password simple aaa 
authorization-attribute user-role network-admin work-directory flash:/ 
service-type https 
quit 
netconf soap https enable 
quit
```

2. 执行set_static_route_table为配置静态路由 
   执行delete_static_route_table.py为删除静态路由
```
把需要下的配置写在manager.py里面，netconf接口参照 doc/Comware V7 StaticRoute NETCONF XML API Configuration Reference

例如，静态路由的信息为： 
DestVrfIndex = '0' 
DestTopologyIndex = '0' 
Ipv4Address = '3.3.3.3' 
Ipv4PrefixLength = '24' 
NexthopVrfIndex = '0' 
NexthopIpv4Address = '4.4.4.1' 
IfIndex = '0'
```


# 以上代码由H3C厂家提供
