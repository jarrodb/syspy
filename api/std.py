from tornado import web, escape
from libs.torn.decorators import user_passes
from libs.torn.handlers import ApiHandler
from mongokit import ObjectId
import subprocess
import os

class StdApiHandler(ApiHandler):
    def check_xsrf_cookie(self):
        pass


class StdHandler(StdApiHandler):
    STDLIB = {
        'mkdir': '_mkdir',
        }

    def post(self, cmd):
        error = None
        try:
            std_f = getattr(self, self.STDLIB[cmd])
            std_f()
        except KeyError, e:
            self.write_error('stdlib cmd not found')
        except Exception, e:
            self.write_error('%s' % e)
        else:
            self.write({'success': True})

    def _mkdir(self):
        _dir = self.get_argument('dir', None)
        try:
            if not _dir: raise Exception('dir must be populated')
            if os.path.exists(_dir): raise Exception('dir exists')

            args = ['mkdir',_dir]
            p = self._system_call(args)
        except Exception, e:
            self.write_error(e.message)
        else:
            self.write({'success': True})
        finally:
            self.finish()

    def _system_call(self, args):
        p = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
        stdout, stderr = p.communicate()
        if stderr:
            raise Exception('%s failed' % (args[0]))
        return p

