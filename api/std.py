from tornado import web, escape
from libs.torn.decorators import user_passes
from libs.torn.handlers import ApiHandler
from mongokit import ObjectId
from libs.std import Stdlib

#curl -v -H "Content-Type: application/json" -X POST -d 'args=/dir' \
#http://localhost:8887/api/1/stdlib/mkdir

class StdApiHandler(ApiHandler):
    def check_xsrf_cookie(self):
        pass


class StdHandler(StdApiHandler):
    @web.authenticated
    def post(self, cmd):
        stdlib = Stdlib()
        args = self.get_argument('args', '')
        args = args.split()

        res = stdlib.command(cmd, args)

        if 'error' in res:
            self.write_error(res['error'])
        else:
            self.write({'success': res['success']})

