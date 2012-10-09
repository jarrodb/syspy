from tornado import web, escape
from libs.torn.forms import TornadoMultiDict
from libs.torn.decorators import user_passes
from forms.postfix import UserForm
from models.postfix import User, Domain, Forwardings
from handler import PostfixApiHandler
from settings import settings

class UserHandler(PostfixApiHandler):
    @web.authenticated
    def get(self):
        query = self._query_obj(User)

        _id = self.get_argument('id', None)
        _email = self.get_argument('email', None)
        _domain = self.get_argument('domain', None)
        if _id:
            query = query.filter_by(id=_id)
        elif _email:
            query = query.filter_by(email=_email)
        elif _domain:
            # if domain exists, filter by it
            query = query.filter(User.email.endswith('@%s' % _domain))

        self.write({'response': self._dict_from_sql_rows(query.all())})

    @web.authenticated
    def put(self):
        form = UserForm(TornadoMultiDict(self.request.arguments))
        try:
            for field in form:
                # validate individual fields that are populated
                if field.data: field.validate()
            _u = User()
            form.populate_obj(_u)
            self.db.save_or_update(_u)
            self.db.commit()
        except Exception, e:
            self.write({
                'error': e,
                'form': form.errors,
                })
        else:
            self.write({
                'response': self._row_dict(_u),
                })

    @web.authenticated
    def post(self):
        form = UserForm(TornadoMultiDict(self.request.arguments))
        try:
            self._validate_or_exception(form)

            _domain = self._domain_from_user(form.email.data)
            if not self._domain_exists(_domain):
                raise ValueError('domain does not exist.')

            _u = User(
                email=form.email.data,
                password=form.password.data,
                quota=form.quota.data,
                )

            self.db.add(_u) #

            _user, _domain = _u.email.split('@')
            maildir = "%s/%s/%s/Maildir" % (self.PATH, _domain, _user)
            self._mkdir(maildir)
            self._chown(maildir, settings.postfix_uid, settings.postfix_gid)

            self.db.commit()
        except Exception, e:
            self.write({
                'form': form.errors,
                'error': '%s' % (e),
                })
            #self.write_error('%s' % (e))
        else:
            self.write({
                'response': self._row_dict(_u),
                })

