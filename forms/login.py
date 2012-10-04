import wtforms

class LoginForm(wtforms.Form):
    username = wtforms.TextField(
        'E-mail Address',
        [wtforms.validators.Length(min=5)]
        )
    password = wtforms.PasswordField('Password')

