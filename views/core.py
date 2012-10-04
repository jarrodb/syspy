from tornado import web, escape

from libs.torn.handlers import ViewHandler
from libs.torn.forms import TornadoMultiDict
from forms.login import LoginForm


class IndexHandler(ViewHandler):
    tpl = 'index.html'

    @web.authenticated
    def get(self):
        self.render(self.tpl, **{
            })


class LoginHandler(ViewHandler):
    tpl = 'login.html'

    def get(self):
        self.render(self.tpl, **{
            'loginform': LoginForm(),
            })

    def post(self):
        try:
            loginform = LoginForm(TornadoMultiDict(self.request.arguments))
            self._validate_or_exception(loginform)
            user = self.auth_user(
                loginform.username.data,
                loginform.password.data
                )
        except Exception, e:
            self.render(self.tpl, **{
                'error': e.message,
                'loginform': loginform,
                })
        else:
            self.set_current_user(str(user.get('_id')))
            self.redirect(self.reverse_url('index'))


class LogoutHandler(ViewHandler):
    def get(self):
        self.clear_current_user()
        self.redirect(self.reverse_url('index'))

