from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('postjob/', views.postJob, name='postjob'),
    path('currentlyOpening/', views.currentOpeningJobs, name='currentOpeningJobs'),
    path('allJobs/', views.allJobs, name='allJobs'),
    path('<slug:job_slug>/', views.jobDetail, name='jobDetail')
]
