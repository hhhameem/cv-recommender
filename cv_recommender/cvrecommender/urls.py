from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('postjob/', views.postJob, name='postjob'),
    path('editjob/<int:pk>', views.editjob, name='editjob'),
    path('currentlyOpening/', views.currentOpeningJobs, name='currentOpeningJobs'),
    path('allJobs/', views.allJobs, name='allJobs'),
    path('job/<slug:job_slug>/', views.jobDetail, name='jobDetail'),
    path('job/category/<str:job_cat>', views.jobCategory, name='jobCategory')
]
