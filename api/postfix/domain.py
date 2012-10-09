from tornado import web, escape
from libs.torn.forms import TornadoMultiDict
from libs.torn.decorators import user_passes
from forms.postfix import UserForm, DomainForm
from models.postfix import User, Domain, Forwardings
from handler import PostfixApiHandler
from settings import settings

class DomainHandler(PostfixApiHandler):
    @web.authenticated
    def get(self):
        query = self._query_obj(Domain)

        _id = self.get_argument('id', None)
        _domain = self.get_argument('domain', None)

        if _id:
            query = query.filter_by(id=_id)
        elif _domain:
            # if domain exists, filter by it
            query = query.filter_by(domain=_domain)

        rows = query.all()
        self._clean_rows(rows)
        self.write({'response': self._dict_from_sql_rows(rows)})

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
        form = DomainForm(TornadoMultiDict(self.request.arguments))
        try:
            self._validate_or_exception(form)

            _domain = self.get_argument('domain')
            if self._domain_exists(_domain):
                raise ValueError('domain already exists.')

            _d = Domain(
                domain=form.domain.data,
                )

            self.db.add(_d) # add insert to the query

            # create the domain directory (exception before commit)
            domain_dir = "%s/%s" % (self.PATH, _domain)
            self._mkdir(domain_dir)
            self._chown(domain_dir, settings.postfix_uid, settings.postfix_gid)

            self.db.commit()
        except Exception, e:
            self.write({
                'form': form.errors,
                'error': '%s' % (e),
                })
        else:
            self.write({
                'response': self._row_dict(_d),
                })

