# -*- coding:utf-8 -*-

import urllib2
import httplib
from string import Template
from xml.etree import ElementTree as ET


MESSAGE_ID = "101"
LANGUAGE_CH = "zh-cn"
LANGUAGE_EN = "en"

NS_HELLO = "{http://www.%s.com/netconf/base:1.0}"
NS_DATA = "{http://www.%s.com/netconf/data:1.0}"
HELLO = """<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
   <env:Header>
      <auth:Authentication env:mustUnderstand="1" xmlns:auth="http://www.%s.com/netconf/base:1.0">
         <auth:UserName>%s</auth:UserName>
         <auth:Password>%s</auth:Password>
      </auth:Authentication>
   </env:Header>
   <env:Body>
      <hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
         <capabilities>
            <capability>urn:ietf:params:netconf:base:1.0</capability>
         </capabilities>
      </hello>
   </env:Body>
</env:Envelope>"""

CLOSE = """<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
   <env:Header>
      <auth:Authentication env:mustUnderstand="1" xmlns:auth="http://www.$OEM.com/netconf/base:1.0">
         <auth:AuthInfo>$AuthInfo</auth:AuthInfo>
         <auth:Language>$Language</auth:Language>
      </auth:Authentication>
   </env:Header>
   <env:Body>
     <rpc message-id="$messageid"
          xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
       <close-session/>
     </rpc>
   </env:Body>
</env:Envelope>"""

EDIT_HEAD = """<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
  <env:Header>
    <auth:Authentication env:mustUnderstand="1" xmlns:auth="http://www.$OEM.com/netconf/base:1.0">
      <auth:AuthInfo>$AuthInfo</auth:AuthInfo>
      <auth:Language>$Language</auth:Language>
    </auth:Authentication>
  </env:Header>
  <env:Body>
    <rpc message-id="$messageid" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <edit-config>
             <target>
          <running/>
        </target>
            <default-operation>merge</default-operation>
        <test-option>set</test-option>
        <error-option>continue-on-error</error-option>
        <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
          <top xmlns="http://www.$OEM.com/netconf/config:1.0" >"""

EDIT_TAIL = """ </top>
        </config>
      </edit-config>
    </rpc>
  </env:Body>
</env:Envelope>"""

GET_HEADER = """<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
  <env:Header>
    <auth:Authentication env:mustUnderstand="1" xmlns:auth="http://www.$OEM.com/netconf/base:1.0">
      <auth:AuthInfo>$AuthInfo</auth:AuthInfo>
      <auth:Language>$Language</auth:Language>
    </auth:Authentication>
  </env:Header>
  <env:Body>
    <rpc message-id="$messageid" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <get>
        <filter type="subtree">
          <top xmlns="http://www.$OEM.com/netconf/data:1.0" xmlns:base="http://www.$OEM.com/netconf/base:1.0" xmlns:netconf="urn:ietf:params:xml:ns:netconf:base:1.0">"""

GET_TAIL = """</top></filter>
         </get>
      </rpc>
   </env:Body>
</env:Envelope>"""

GET_BULK_HEADER = """<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
  <env:Header>
    <auth:Authentication env:mustUnderstand="1" xmlns:auth="http://www.$OEM.com/netconf/base:1.0">
      <auth:AuthInfo>$AuthInfo</auth:AuthInfo>
      <auth:Language>$Language</auth:Language>
    </auth:Authentication>
  </env:Header>
  <env:Body>
    <rpc message-id="$messageid" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <get-bulk>
        <filter type="subtree">
          <top xmlns="http://www.$OEM.com/netconf/data:1.0"  xmlns:h3c="http://www.$OEM.com/netconf/data:1.0" xmlns:base="http://www.$OEM.com/netconf/base:1.0" xmlns:netconf="urn:ietf:params:xml:ns:netconf:base:1.0">"""

GET_BULK_TAIL = """</top></filter>
         </get-bulk>
      </rpc>
   </env:Body>
</env:Envelope>"""

CLI_EXEC_HEAD = """<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
   <env:Header>
      <auth:Authentication env:mustUnderstand="1" xmlns:auth="http://www.$OEM.com/netconf/base:1.0">
         <auth:AuthInfo>$AuthInfo</auth:AuthInfo>
         <auth:Language>$Language</auth:Language>
      </auth:Authentication>
   </env:Header>
   <env:Body>
      <rpc message-id="$messageid" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
         <CLI>
          <Execution>"""

CLI_EXEC_TAIL = """</Execution>
        </CLI>
      </rpc>
   </env:Body>
</env:Envelope>"""

CLI_CONF_HEAD = """<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
   <env:Header>
      <auth:Authentication env:mustUnderstand="1" xmlns:auth="http://www.$OEM.com/netconf/base:1.0">
         <auth:AuthInfo>$AuthInfo</auth:AuthInfo>
         <auth:Language>$Language</auth:Language>
      </auth:Authentication>
   </env:Header>
   <env:Body>
      <rpc message-id="$messageid" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
         <CLI>
          <Configuration>"""

CLI_CONF_TAIL = """</Configuration>
        </CLI>
      </rpc>
   </env:Body>
</env:Envelope>"""

SESSION = """
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
   <env:Header>
      <auth:Authentication env:mustUnderstand="1" 
      xmlns:auth="http://www.$OEM.com/netconf/base:1.0">
         <auth:AuthInfo>$AuthInfo</auth:AuthInfo>
         <auth:Language>$Language</auth:Language>
      </auth:Authentication>
   </env:Header>
   <env:Body>
      <rpc message-id="$messageid" 
      xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
       <get-sessions/>
      </rpc>
   </env:Body>
</env:Envelope>"""


class NETCONF(object):
    def __init__(self, ip, user, password):
        url = 'https://%s:832/soap/netconf/' % ip
        self.url = url
        self.oem = 'h3c'
        self.messageid = MESSAGE_ID
        self.Language = LANGUAGE_EN
        self.ns_data = NS_DATA % self.oem
        self.user = user
        self.password = password
        self.AuthInfo = None

    def close_session(self):
        if self.AuthInfo is not None:
            close_template = Template(CLOSE)
            close_msg = close_template.substitute(OEM=self.oem,
                                                  AuthInfo=self.AuthInfo,
                                                  Language=self.Language,
                                                  messageid=self.messageid)
            try:
                req = urllib2.Request(self.url, close_msg)
                resp = urllib2.urlopen(req)
                self.AuthInfo = None
            except urllib2.URLError, err:
                print("Close session failed: %s", err)

    def request(self, req_msg):
        msg = Template(req_msg)
        MSG = msg.substitute(OEM=self.oem, Language=self.Language,
                             messageid=self.messageid,
                             AuthInfo=self.AuthInfo)
        req = urllib2.Request(self.url, MSG)
        if req is not None:
            try:
                resp = urllib2.urlopen(req, timeout=8)
                if resp is not None:
                    buf = resp.read()
                    return buf
                else:
                    print('Failed to open url %s', self.url)
            except Exception as e:
                print("Request failed %s, url %s", e, self.url)

    def get_session(self):
        if self.AuthInfo is not None:
            verify_msg = self.request(SESSION)
            root = ET.fromstring(verify_msg)
            is_return = True
            for element in root.iter("faultstring"):
                if element.text == 'Invalid session':
                    is_return = False
                    break
            if is_return is True:
                return

        hello_msg = HELLO % (self.oem, self.user, self.password)
        req_hello = urllib2.Request(self.url, hello_msg)
        try:
            resp_hello = urllib2.urlopen(req_hello, timeout=3)
        except urllib2.URLError, err:
            if hasattr(err, "reason"):
                print('Failed to connect %s, Err:%s', self.url, err.reason)
            elif hasattr(err, "code"):
                print('Request failed, Err:%s', err.code)
            return
        except httplib.HTTPException as e:
            print("get session with HTTPException %s", e)
            return

        buf_hello = resp_hello.read()
        root = ET.fromstring(buf_hello)
        ns = NS_HELLO % self.oem
        for auth in root.iter(ns + "AuthInfo"):
            self.AuthInfo = auth.text
            break

    def Get(self, body, *tags):
        self.get_session()
        get_msg_tmp = GET_HEADER + body + GET_TAIL
        buf_get = self.request(get_msg_tmp)
        root = ET.fromstring(buf_get)
        dict_ret = {}
        for element in tags:
            tag = self.ns_data + element
            for label in root.iter(tag):
                dict_ret[element] = label.text
                break
        return dict_ret

    def GetNext(self, body, *tags):
        self.get_session()
        getall_msg_tmp = GET_BULK_HEADER + body + GET_BULK_TAIL
        buf_get = self.request(getall_msg_tmp)
        dict_ret = {}
        if buf_get is not None:
            root = ET.fromstring(buf_get)

            for element in tags:
                tag = self.ns_data + element
                for label in root.iter(tag):
                    dict_ret[element] = label.text
                    break
        return dict_ret

    def get_bulk(self, body, *tags):
        self.get_session()
        get_msg_tmp = GET_HEADER + body + GET_TAIL
        buf_get = self.request(get_msg_tmp)
        if buf_get is None:
            return
        root = ET.fromstring(buf_get)
        dict_ret = {}
        for element in tags:
            tag = self.ns_data + element
            dict_ret.setdefault(element, [])
            for label in root.iter(tag):
                dict_ret[element].append(label.text)
        return dict_ret
    
    def get_bulk2(self, body, *tags):
        get_msg_tmp = GET_HEADER + body + GET_TAIL
        buf_get = self.request(get_msg_tmp)

        if (buf_get is not None and
            (buf_get.find('env:Fault') != -1) and
                (buf_get.find('Invalid session') != -1)):
            self.get_session()
            buf_get = self.request(get_msg_tmp)

        if buf_get is None:
            return
        root = ET.fromstring(buf_get)
        dict_ret = {}
        for element in tags:
            tag = self.ns_data + element
            dict_ret.setdefault(element, [])
            for label in root.iter(tag):
                dict_ret[element].append(label.text)
        return dict_ret

    def Set(self, body):
        self.get_session()
        set_msg_tmp = EDIT_HEAD + body + EDIT_TAIL
        return self.request(set_msg_tmp)

    def Exec(self, cmd):
        self.get_session()
        exec_msg_tmp = CLI_EXEC_HEAD + cmd + CLI_EXEC_TAIL
        return self.request(exec_msg_tmp)

    def Config(self, cmd):
        self.get_session()
        conf_msg_tmp = CLI_CONF_HEAD + cmd + CLI_CONF_TAIL
        return self.request(conf_msg_tmp)
