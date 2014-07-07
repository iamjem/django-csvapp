from django.contrib.auth.forms import AuthenticationForm


class BootstrapAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
