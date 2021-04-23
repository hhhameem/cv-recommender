from django import forms
from .models import Job


class DateInput(forms.DateInput):
    input_type = 'date'


class JobPostForm(forms.ModelForm):
    starting_date = forms.DateField(widget=DateInput)
    deadline = forms.DateField(widget=DateInput)

    class Meta:
        model = Job
        fields = ('title', 'slug', 'company_name', 'starting_date',
                  'deadline', 'salary', 'vacancy', 'job_category',
                  'job_type', 'email', 'phone', 'company_website',
                  'logo', 'address', 'division', 'description',
                  'responsibility', 'min_education', 'cgpa',
                  'experience', 'skill_req', 'skill_bonus', 'status')


class EditJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('title', 'slug', 'company_name',
                  'starting_date', 'deadline', 'status',)

    def __init__(self, *args, **kwargs):
        super(EditJobForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['readonly'] = True
