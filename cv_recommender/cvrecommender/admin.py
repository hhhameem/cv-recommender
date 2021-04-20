from django.contrib import admin
from .models import Job
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
