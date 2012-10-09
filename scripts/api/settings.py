from tornado.util import ObjectDict

settings_ = dict(
    site_url = 'http://127.0.0.1:8887',

    api_ngin = 'postfix',

    sys_token = '3j9d02d20',
    sys_secret = '32u9e032hd23',
    sys_apiver = '1',
)

settings = ObjectDict(settings_)
