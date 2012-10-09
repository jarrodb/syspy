from tornado import web, escape

from libs.torn.handlers import ViewHandler
from libs.torn.forms import TornadoMultiDict


class IndexHandler(ViewHandler):
    tpl = 'index.html'

    def get(self):
        self.render(self.tpl, **{
            })


class LoginHandler(ViewHandler):
    tpl = 'login.html'

    def get(self):
        self.render(self.tpl, **{
            })

    def post(self):
        try:
            #loginform = LoginForm(TornadoMultiDict(self.request.arguments))
            #self._validate_or_exception(loginform)
            #user = self.auth_user(
                #loginform.username.data,
                #loginform.password.data
                #)
            pass
        except Exception, e:
            #self.render(self.tpl, **{
                #'error': e.message,
                #'loginform': loginform,
                #})
            pass
        else:
            self.set_current_user(str(user.get('_id')))
            self.redirect(self.reverse_url('index'))


class LogoutHandler(ViewHandler):
    def get(self):
        self.clear_current_user()
        self.redirect(self.reverse_url('index'))

