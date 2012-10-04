import json
import wtforms
import httplib
import tornado.web
import os
from hashlib import md5
from datetime import datetime, date
from mongokit import ObjectId
from settings import settings


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler,self).__init__(*args, **kwargs)
        self.conn = self.application.settings.get('connection')
        self.db = self.conn[settings.mongo_dbname]
        self._httplib = httplib

    def get_current_user(self):
        try:
            _u = json.loads(self.get_secure_cookie('authed_user'))
            # query memcache here
            return self.conn.User.find_one({'_id':ObjectId(_u['user'])})
        except:
            return None

    def set_current_user(self, user):
        self.set_secure_cookie(
            'authed_user',
            json.dumps({'user':str(user)}),
            expires_days=3,
            )

    def clear_current_user(self):
        self.set_secure_cookie('authed_user', '')

    def auth_user(self, email, passwd):
        _u = self.conn.User.find_one({
            'email': email,
            'password': md5(passwd).hexdigest()
            })
        if not _u: raise ValueError('Login Incorrect')
        return _u

    def get_and_clear_secure_cookie(self, key):
        val = self.get_secure_cookie(key, None)
        self.set_secure_cookie(key, '')
        return val

    def get_args_uri(self, exclude=[]):
        q = '?'
        for key in self.request.arguments:
            if not key in exclude:
                for val in self.get_arguments(key):
                    q += '%s=%s&' % (key, val)
        return q

    def get_args_form(self, exclude=[]):
        inputs = ''
        tpl = '<input type="hidden" name="%s" value="%s">'
        for key in self.request.arguments:
            if not key in exclude:
                for val in self.get_arguments(key):
                    inputs += tpl % (key, val)
        return inputs

    def render_string(self, template_name, **kwargs):
        kwdef = {
            'error': None,
            'query': None,
            'updated': None,
            'notification': None,
            'nav_active': 'home',
            'site_url': settings.site_url,
            }
        kwdef.update(kwargs)

        return super(BaseHandler, self).render_string(template_name, **kwdef)

    # private
    def _get_remote_addr(self):
        remote_ip = self.request.headers.get('X-Forwarded-For', None)
        if not remote_ip:
            remote_ip = self.request.remote_ip
        return remote_ip


class ViewHandler(BaseHandler):
    """
    """
    def __init__(self, *args, **kwargs):
        super(ViewHandler,self).__init__(*args, **kwargs)

    def _validate_or_exception(self, form):
        if not form.validate():
            raise wtforms.validators.ValidationError('Invalid Form')

    def _update_doc_from_form(self, doc, form, exclude=None):
        # exclude should be a list of strings that are form elements
        # that should not be assigned
        if not exclude or not isinstance(exclude, list):
            exclude = []

        # Let's assume something changed if you clicked 'Update'
        # You can refactor later ...
        # ... yea right
        change = 1

        for field in form:
            name = field.short_name # Use short_name for FieldLists
            data = field.data

            # compare or just assign it
            if isinstance(data, list):
                # strip empty items
                data = filter(None, data)
                # assume the form validated the data accordingly

            elif isinstance(data, str) or isinstance(data, unicode):
                # for good measure
                data = data.decode('utf-8')

            elif isinstance(data, date):
                # mongokit documents only support datetime, DOH!
                data = datetime(data.year, data.month, data.day)

            if not name in exclude and data:
                setattr(doc, name, data)



class ApiHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(ApiHandler,self).__init__(*args, **kwargs)

    def write_error(self, error, status_code = httplib.BAD_REQUEST):
        self.set_status(status_code)
        self.write({
            'error': error
            })


