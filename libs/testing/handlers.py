import tornado.escape
import httplib
import urllib
import json
from tornado.testing import AsyncHTTPTestCase, LogTrapTestCase
from libs.testing.mixin import HTTPClientMixin

try:
    from pymongo import json_util
except:
    from bson import json_util

class TornadoTestCase(HTTPClientMixin, AsyncHTTPTestCase):
    _httplib = httplib

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)

    def _d(self, url, **kwargs):
        body_type = kwargs.get('body_type', None)
        body = kwargs.get('body', None)
        headers = kwargs.get('headers', {})
        if body:
            if not body_type:
                body = urllib.urlencode(body)
            elif body_type == 'json':
                headers['Content-Type'] = 'application/json'
                body = json.dumps(body,default=json_util.default)
            else:
                raise ValueError('body_type %s unimplemented' % body_type)

        args = {
            'method': kwargs.get('method', 'GET'),
            'headers': headers,
            'body': body,
            }

        self.http_client.fetch(
            self.get_url(url),
            self.stop,
            **args
            )

        response = self.wait()

        d = {}
        try:
            if 'application/json' in response.headers.get('Content-Type'):
                d = tornado.escape.json_decode(response.body)
        except:
            pass

        d['response_code'] = response.code
        d['response_body'] = response.body
        return d


class ApiTest(TornadoTestCase):

    def get_app(self):
        from app import tornapp
        return tornapp

