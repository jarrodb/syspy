from tornado import web, escape
from libs.torn.decorators import user_passes
from libs.torn.handlers import ApiHandler
from mongokit import ObjectId
from libs.std import Stdlib

from models.postfix import User, Domain, Forwardings

class PostfixApiHandler(ApiHandler):
    def check_xsrf_cookie(self):
        pass

    def _row_dict(self, row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = getattr(row, column.name)
        return d


class UserHandler(PostfixApiHandler):
    @web.authenticated
    def get(self):
        res = self.db.query(User) # query for the User model

        domain = self.get_argument('domain', None)
        if domain:
            # if domain exists, filter by it
            res = res.filter(User.email.endswith('@%s' % domain))

        res = res.all() # return all results

        users = []
        # convert User object to dict for json
        [users.append(self._row_dict(r)) for r in res]

        self.write({'users': users})

    @web.authenticated
    def post(self):
        # create user
        pass

