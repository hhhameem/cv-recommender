from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Applicant, Recruiter


Role = (
    ('applicant', 'Applicant'),
    ('recruiter', 'Recruiter'),
)


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateUserForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Role)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'user_type', 'password1', 'password2')

    # check both password field if they match
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Password Doesn\'t Match")
        return cd['password2']


class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RecruiterEditForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = ('phone', 'organization', 'details', 'image')

    def __init__(self, *args, **kwargs):
        super(RecruiterEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ApplicantEditForm(forms.ModelForm):
    dob = forms.DateField(widget=DateInput)

    class Meta:
        model = Applicant
        fields = ('phone', 'work_exp', 'summary', 'gender',
                  'address', 'dob', 'language', 'website', 'category', 'image')

    def __init__(self, *args, **kwargs):
        super(ApplicantEditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
