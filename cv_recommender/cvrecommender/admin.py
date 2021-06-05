from django.contrib import admin
from .models import Job, JobApplication
# Register your models here.


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('recruiter', 'title', 'company_name',
                    'job_category', 'status',  'email',
                    'phone', 'publish', 'salary', 'vacancy', )
    list_filter = ('publish', 'status', 'job_category')
    search_fields = ('title', 'company_name', 'email')
    date_hierarchy = 'publish'
    ordering = ('publish',)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'score', 'first_name',
                    'email', 'phone', 'apply_time')
    list_filter = ('apply_time',)
    search_fields = ('applicant', 'job', 'email')
    ordering = ('apply_time',)
