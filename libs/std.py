import subprocess
import os

class Stdbase(object):
    def error(self, message):
        return {'error': message}

    def success(self, message):
        return {'success': message}


class Stdlib(Stdbase):
    def __init__(self):
        self.STDLIB = {
            'mkdir': self._mkdir,
            'chown': self._chown,
            'rmdir': self._rmdir,
        }

    def command(self, cmd, args=[]):
        try:
            std_f = self.STDLIB[cmd]
            p = std_f(cmd, args)
        except KeyError, e:
            return self.error('stdlib command not found')
        except Exception, e:
            return self.error('%s' % (e.message))
        else:
            return self.success('%s executed.' % (cmd))


    def _mkdir(self, cmd, args):
        _dir = args[0]
        if not _dir: raise Exception('dir must be specified')
        if os.path.exists(_dir): raise Exception('unable to create dir')

        return self._system_call(cmd, args)

    def _rmdir(self, cmd, args):
        _dir = args[0]
        if not _dir: raise Exception('dir must be specified')
        if not os.path.exists(_dir): raise Exception('dir does not exist')

        return self._system_call(cmd, args)

    def _chown(self, cmd, args):
        return self._system_call(cmd, args)

    def _system_call(self, cmd, args):
        args.insert(0, cmd) # ['cmd','arg1','arg2',etc..]
        p = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
        stdout, stderr = p.communicate()
        if stderr:
            raise Exception('%s failed' % (args[0]))

        return p

