#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import logging

def _encode_params(**kw):
    """ Encode parameters. """
    args = []
    for k, v in kw.iteritems():
        qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
        args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(args)

class HttpHelper:
#    # create
#    http = HttpHelper()
#    # set cookies and gsid
#    http.add_cookie(name, value, domain)
    """ Http 封装类 """
    def __init__(self):
        self.cj = cookielib.CookieJar()
        self._GET = 0
        self._POST = 1
    def get(self, url, **kw):
        logging.debug('GET %s' % url)
        return self._http_call(url, self._GET, **kw)
    def post(self, url, **kw):
        logging.debug('POST %s' % url)
        return self._http_call(url, self._POST, **kw)
    def add_cookie(self, name, value, domain):
        ck = cookielib.Cookie(version=0, name=name, value=value, port=None, port_specified=False, domain=domain, domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.cj.set_cookie(ck)
    def _http_call(self, url, method, **kw):
        params = _encode_params(**kw)   #params is a str
        if method == self._GET:
            http_url = '%s?%s' % (url, params) if params!='' else url
            http_body = None
        else:
            http_url = url
            http_body = params
       	req = urllib2.Request(
	    	url=http_url, 
	    	data=http_body,
	    	headers=self._getHeaders(self.cj)
	    	)
       	opener = urllib2.build_opener()
       	resp = opener.open(req)
       	html = resp.read()
        # Load the cookies from the response
        str_set_ck = resp.headers.get('set-cookie')
        if str_set_ck:
            m = re.match(r'(.*?)=(.*?);', str_set_ck)
            if m:
                if m.group(2) != 'deleted':
                    self.add_cookie(m.group(1), m.group(2), '')
        return html
    def _getHeaders(self, cj):
        headers = {
            'Accept-Encoding' : 'utf-8',
            'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Cookie' : self._makeCookieHeader(cj)
        }
        return headers
    def _makeCookieHeader(self, cj):
        """ cookielib.CookieJar to str_Cookie """
        cookieHeader = ""
        for i in cj._cookies.itervalues():
            for j in i['/'].itervalues():
                cookieHeader += '%s=%s;' % (j.name, j.value)
        print cookieHeader
        return cookieHeader

if __name__ == '__main__':
    url = 'http://www.baidu.com'
    http = HttpHelper()
    html = http.get(url)
    print html

