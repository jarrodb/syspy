from tornado import web, escape
from libs.torn.decorators import user_passes
from libs.torn.handlers import ApiHandler
from mongokit import ObjectId


class StdApiHandler(ApiHandler):
    pass


class StdHandler(UserApiHandler):
    LIB = {
        'mkdir': '_mkdir',
        }

    def post(self, cmd):
        error = None
        try:
            std_f = self.LIB[cmd]
        except:
            self.write_error('stdlib cmd not found')
        else:
            self.write({'success': True})

    def _mkdir(self):
        pass

