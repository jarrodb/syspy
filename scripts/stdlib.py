#!/bin/sh
import sys
sys.path.append("..")

from settings import settings
import httplib
import requests

class Stdlib(object):
    def __init__(self):
        self.COMMANDS = {
            'mkdir': self._mkdir,
            'chown': self._chown,
            }

        self.url = settings.site_url
        self.payload = {}
        self.headers = {
            'Token' : settings.sys_token,
            'Secret': settings.sys_secret,
            }

        self._requests = requests
        self._httplib = httplib

    def __getattr__(self, cmd):
        try:
            return self.COMMANDS[cmd]
        except:
            raise ValueError('stdlib %s not found' % (cmd))

    def command(self, cmd, args):
        url = self._get_api_url(cmd)
        self.payload['args'] = args

        r = self._requests.post(
            url,
            headers=self.headers,
            data=self.payload,
            )

        if r.status_code != 200:
            error = r.json.get('error', '')
            raise httplib.HTTPException("%s: %s" % (r.status_code, error))
        else:
            return r.json

    def _mkdir(self, args):
        return self.command('mkdir', args)

    def _chown(self, args):
        return self.command('chown', args)

    def _get_api_url(self, resource):
        return '%s/api/%s/stdlib/%s' % (
            self.url,
            settings.sys_apiver,
            resource
            )

if __name__ == '__main__':
    pass

