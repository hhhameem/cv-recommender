from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

# Create your models here.
GENDER_CHOICE = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)

JOB_CATEGORY = (
    ('webdeveloper', 'Web Developer'),
    ('softwareengineer', 'Software Engineer'),
    ('mobileapplication', 'Mobile Application'),
)


class Recruiter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, blank=True, null=True)
    organization = models.CharField(max_length=100)
    details = models.TextField()
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'


class Applicant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, blank=True, null=True)
    work_exp = models.CharField(max_length=50, blank=True, null=True)
    summary = models.TextField(max_length=255)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICE, default='Male')
    address = models.TextField(max_length=100)
    dob = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=100)
    website = models.URLField()
    image = models.ImageField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=JOB_CATEGORY,
                                default='Web Developer')

    def __str__(self):
        return f'{self.user.username}'
