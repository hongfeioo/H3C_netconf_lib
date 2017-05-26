# -*- coding:utf-8 -*-

import urllib
import urllib2
import base64
import json

class RESTFUL(object):
    def __init__(self, ip, user, password):
        self.host = ip
        self.user = user
        self.password = password
        self.token = None
        self.getSession()

    def fillheader(self, headers):
        headers['Accept-Encoding'] = 'gzip,deflate'
        headers['Content-Type'] = 'application/json'
        headers['Host'] = self.host
        headers['Connection'] = 'Keep-Alive'
        headers['User-Agent'] = 'Apache-HttpClient/4.1.1 (java 1.5)'

    def request(self, url, body, headers, method):
        req = urllib2.Request(url, data=body, headers=headers)
        req.get_method = lambda: '%s' % method
        try:
            resp = urllib2.urlopen(req, timeout=10)
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                LOG.error("%s %s failed, reason:%s" % (method, url, e.reason))
            elif hasattr(e, "code"):
                LOG.error("server couldn't fulfill the request, Error:%s" %
                          e.code)
            return None
        except Exception as excpt:
            LOG.error("restful request failed, Error:%s" % excpt)
            return None

        buf = resp.read()
        return buf

    def getSession(self):
        headers = {}
        self.fillheader(headers)
        headers['Authorization'] = ("Basic %s" %
                                    base64.encodestring("%s:%s" %
                                                        (self.user,
                                                         self.password)))
        headers['Content-Length'] = 0
        url = 'https://%s:443/api/v1//tokens HTTP/1.1' % self.host

        buf = self.request(url, None, headers, 'POST')
        if buf is None:
            LOG.warn("getSession request failed")
            return
        token = json.loads(buf)
        self.token = token['token-id'].encode()

    def post(self, table, body_dict):
        headers = {}
        self.fillheader(headers)
        headers['X-Auth-Token'] = self.token

        body = json.dumps(body_dict)
        headers['Content-Length'] = len(body)
        url = 'https://%s:443/api/v1/%s HTTP/1.1' % (self.host, table)

        req = urllib2.Request(url, data=body, headers=headers)
        method = 'POST'
        req.get_method = lambda: '%s' % method
        try:
            resp = urllib2.urlopen(req, timeout=10)
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                if e.reason == 'Unauthorized':
                    self.getSession()
                    headers['X-Auth-Token'] = self.token
                    self.request(url, body, headers, 'POST')
                    return
                else:
                    LOG.error("%s %s failed, reason:%s" % (method, url, e.reason))
            elif hasattr(e, "code"):
                LOG.error("server couldn't fulfill the request, Error:%s" %
                          e.code)
        return

    def convert(self, table_index):
        table = table_index.split("?index=")
        url = table[1].split("&partial=")
        url_dict = {'index':url[0]}
        if len(url) > 1:
            url_dict['partial'] = url[1]
        return "%s?%s" %(table[0], urllib.urlencode(url_dict))

    def set(self, table_index, body, method):
        headers = {}
        self.fillheader(headers)
        headers['X-Auth-Token'] = self.token
        if body is not None:
            headers['Content-Length'] = len(body)

        url = ('https://%s:443/api/v1/%s HTTP/1.1' %
               (self.host, self.convert(table_index)))

        req = urllib2.Request(url, data=body, headers=headers)
        req.get_method = lambda: '%s' % method
        try:
            resp = urllib2.urlopen(req, timeout=10)
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                if e.reason == 'Unauthorized':
                    self.getSession()
                    headers['X-Auth-Token'] = self.token
                    return self.request(url, body, headers, method)
                else:
                    LOG.warn("%s %s failed, reason:%s" % (method, url, e.reason))
            elif hasattr(e, "code"):
                LOG.error("server couldn't fulfill the request, Error:%s" %
                          e.code)
            return None

        buf = resp.read()
        return buf

    def put(self, table_index, body_dict):
        body = json.dumps(body_dict)
        self.set(table_index, body, 'PUT')

    def delete(self, table_index):
        self.set(table_index, None, 'DELETE')

    def get(self, table_index):
        buf = self.set(table_index, None, 'GET')
        return buf