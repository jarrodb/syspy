import wtforms

class UserForm(wtforms.Form):
    email = wtforms.TextField(
        'E-mail',
        [
          wtforms.validators.Required(),
          wtforms.validators.Length(min=5),
          wtforms.validators.Email(message='invalid e-mail'),
          ],
        )
    password = wtforms.PasswordField(
        'Password',
        [wtforms.validators.Required(), wtforms.validators.Length(min=5)],
        )
    quota = wtforms.IntegerField(
        'Quota',
        default='500000000',
        )


class DomainForm(wtforms.Form):
    domain = wtforms.TextField(
        'Domain',
        [
          wtforms.validators.Required(),
          ],
        )

