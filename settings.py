from os import path
from tornado.util import ObjectDict
from libs import dependencies

settings_ = dict(
    debug = True,

    instance_ipv4 = '127.0.0.1',
    instance_port = 8888,

    cookie_secret = 'set_this_in_settings_prod',
    xsrf_cookies = True,

    static_path = path.join(path.dirname(__file__), "static"),
    template_path = path.join(path.dirname(__file__), "tpl"),

    site_url = 'http://127.0.0.1:8888',
    login_url = '/',

    sql_ngin = 'mysql',
    api_ngin = 'postfix',

    postfix_path = '',
    postfix_uid = '',
    postfix_gid = '',
    )

# local overrides untracked by the project
try:
    from settings_prod import settings as settings_prod
    settings_.update(settings_prod)
except ImportError:
    pass

settings = ObjectDict(settings_)

