import json
import wtforms
import httplib
import tornado.web
import os
from hashlib import md5
from datetime import datetime, date

from sqlalchemy.orm import scoped_session, sessionmaker
from mongokit import ObjectId

from models.auth import Auth
from settings import settings


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler,self).__init__(*args, **kwargs)
        self.engine = self.application.settings.get('engine')
        self.session = sessionmaker(bind=self.engine)
        self.db = scoped_session(self.session)
        self._httplib = httplib

    def get_current_user(self):
        try:
            token = self.request.headers.get('Token')
            secret = self.request.headers.get('Secret')
            # query memcache here
            return self.db.query(Auth).filter_by(
                token=token,
                secret=secret
                ).one()
        except:
            return None

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
    def _validate_or_exception(self, form):
        if not form.validate():
            raise wtforms.validators.ValidationError('invalid input')

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

    def _clean_rows(self, rows):
        for row in rows:
            self._clean_row(row)

    def _clean_row(self, row):
        for field in row.__dict__:
            field_val = getattr(row, field)
            if isinstance(field_val, datetime):
                setattr(row, field, field_val.isoformat())

    def _query_obj(self, model):
        # query for the User model
        return self.db.query(model)

    def _dict_from_sql_rows(self, res):
        return [self._row_dict(obj) for obj in res]

    def _row_dict(self, row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = getattr(row, column.name)
        return d

