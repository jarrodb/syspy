#!/bin/sh
import sys
sys.path.append("..")

from settings import settings
import httplib
import requests

class SysObject(object):
    # private:
    def _row_dict(self, row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = getattr(row, column.name)
        return d


class Postfix(SysObject):
    def __init__(self):
        self.RESOURCES = {
            'user': 'user',
            }

        self.url = settings.site_url
        self.payload = {}
        self.headers = {
            'Token' : settings.sys_token,
            'Secret': settings.sys_secret,
            }

        self._requests = requests
        self._httplib = httplib

    def get_users(self, domain=None):
        url = self._get_api_url('user')
        if domain: self.payload['domain'] = domain
        r = self._requests.get(url, params=self.payload, headers=self.headers)
        return r

    def _get_api_url(self, resource):
        return '%s/api/%s/postfix/%s' % (
            self.url,
            settings.sys_apiver,
            resource
            )

if __name__ == '__main__':
    pass

