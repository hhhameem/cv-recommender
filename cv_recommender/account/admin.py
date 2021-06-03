from django.contrib import admin
from .models import Recruiter, Applicant

# Register your models here.


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'organization', 'image')
    search_fields = ('user', 'phone')


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'gender', 'dob', 'category')
    search_fields = ('user', 'phone')
