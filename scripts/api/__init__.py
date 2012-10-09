#!/bin/sh
from settings import settings
import httplib
import requests

from postfix import User, Domain

class Api():
    RESOURCES = {
        'user':User,
        'domain':Domain,
    }

    def __init__(self):
        self.headers = {
            'Token' : settings.sys_token,
            'Secret': settings.sys_secret,
            }
        self.ngin = settings.api_ngin
        self.url = settings.site_url
        self.payload = {}

        self._httplib = httplib
        self._con = Connection(self.ngin, headers=self.headers)

    def __getattr__(self,name):
        obj_name = self.RESOURCES.get(name,None)
        if not obj_name:
            raise NameError('Resource does not exist')
        return obj_name(self._con)


class Connection(object):
    BASE_URL = '%s/api/%s/%s/%s'

    def __init__(self, engine, headers={}):
        self.engine = engine
        self.headers = headers
        self._requests = requests

    def get(self, resource, payload, headers=None):
        headers = self._headers(headers)
        url = self._get_api_url(resource)
        r = self._requests.get(url, params=payload, headers=headers)
        return self._handle_response(r)

    def post(self, resource, payload, headers=None):
        headers = self._headers(headers)
        url = self._get_api_url(resource)
        r = self._requests.post(url, params=payload, headers=headers)
        return self._handle_response(r)

    def _handle_response(self, r_obj):
        if r_obj.status_code == 200:
            return r_obj.json
        error = r_obj.json.get('error', None) if r_obj.json else 'error'
        return {
            'error': error,
            'status_code': r_obj.status_code,
            }

    def _get_api_url(self, resource):
        return self.BASE_URL % (
            settings.site_url,
            settings.sys_apiver,
            self.engine,
            resource,
            )

    def _headers(self, headers):
        return headers if headers else self.headers

if __name__ == '__main__':
    pass
