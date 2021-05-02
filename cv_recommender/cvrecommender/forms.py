from django import forms
from .models import Job, JobApplication


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


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ('first_name', 'last_name', 'email', 'phone',
                  'education_application', 'cgpa_application',
                  'skill_req_application', 'skill_bonus_application',
                  'related_experience_application', 'total_experience_application',
                  'note_application', 'cv_application')

    def __init__(self, *args, **kwargs):
        super(JobApplicationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['readonly'] = True
        self.fields['last_name'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


CITY = (
    ('Dhaka', 'Dhaka'),
    ('Chittagong', 'Chittagong'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Barishal', 'Barishal'),
    ('Sylhet', 'Sylhet'),
    ('Rangpur', 'Rangpur'),
)

JOB_CATEGORY = (
    ('Software Engineering', 'Software Engineering'),
    ('Web Design and Development', 'Web Design & Development'),
    ('Data Science and Analytics', 'Data Science & Analytics'),
    ('Graphic Design', 'Graphic Design'),
    ('Software Quality Assurance', 'Software Quality Assurance'),
    ('Network and System Admin', 'Network & System Admin'),
    ('Information Technology', 'Information Technology'),
    ('Cloud Computing and Engineering', 'Cloud Computing & Engineering'),
    ('Cyber Security', 'Cyber Security'),
)


class SearchForm(forms.Form):
    # title = forms.CharField(max_length=30)
    # city = forms.CharField(max_length=15, choices=CITY)
    # category = forms.CharField(max_length=50, choices=JOB_CATEGORY)
    pass
