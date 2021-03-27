from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


Role = (
    ('applicant', 'Applicant'),
    ('recruiter', 'Recruiter')
)


class CreateUserForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Role)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'user_type', 'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Password Doesn\'t Match")
        return cd['password2']


class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
