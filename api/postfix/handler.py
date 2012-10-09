from libs.torn.handlers import ApiHandler
from models.postfix import User, Domain, Forwardings
from settings import settings
import os

class PostfixApiHandler(ApiHandler):
    PATH = settings.postfix_path

    def check_xsrf_cookie(self):
        pass

    def _domain_exists(self, domain):
        try: res = self.db.query(Domain).filter_by(domain=domain).one()
        except: return False
        else: return True

    def _domain_from_user(self, user):
        try: return user.split('@')[1]
        except: raise ValueError('not a valid e-mail address')

    def _mkdir(self, _dir, _mode=0770):
        if os.path.exists(_dir):
            raise ValueError('directory exists')
        r = os.makedirs(_dir, _mode)

    def _rmdir(self, _dir):
        if not os.path.exists(_dir):
            raise ValueError('directory does not exist')
        r = os.removedirs(_dir)

    def _chown(self, _dir, uid=-1, gid=-1):
        if not os.path.exists(_dir):
            raise ValueError('path does not exist')
        r = os.chown(_dir, uid, gid)
