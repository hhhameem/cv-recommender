from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('postjob/', views.postJob, name='postjob'),
    path('editjob/<int:pk>', views.editjob, name='editjob'),
    path('currentlyOpening/', views.currentOpeningJobs, name='currentOpeningJobs'),
    path('allJobs/', views.allJobs, name='allJobs'),
    path('jobs/', views.allPublishedJobs, name='allPublishedJobs'),
    path('jobs/categories/', views.allCategories, name='allCategories'),
    path('jobs/category/<str:job_cat>',
         views.allPublishedJobs, name='jobCategory'),
    path('jobs/jobdetails/<slug:job_slug>/',
         views.jobDetail, name='jobDetail'),
    path('jobs/<slug:job_slug>/apply/', views.apply, name='apply'),
    path('allappliedjobs/', views.allappliedjobs, name='allappliedjobs'),
]
