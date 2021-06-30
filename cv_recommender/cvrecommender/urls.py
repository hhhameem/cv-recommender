from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('postjob/', views.postJob, name='postjob'),
    path('currentlyOpening/', views.currentOpeningJobs, name='currentOpeningJobs'),
    path('allJobs/', views.allJobs, name='allJobs'),
    path('jobs/', views.allPublishedJobs, name='allPublishedJobs'),
    path('allappliedjobs/', views.allappliedjobs, name='allappliedjobs'),
    path('jobs/categories/', views.allCategories, name='allCategories'),
    path('editjob/<int:pk>', views.editjob, name='editjob'),
    path('jobs/category/<str:job_cat>', views.allPublishedJobs,
         name='jobCategory'),
    path('jobs/jobdetails/<slug:job_slug>/', views.jobDetail,
         name='jobDetail'),
    path('jobs/<slug:job_slug>/apply/', views.apply, name='apply'),
    path('jobs/<slug:job_slug>/applications/', views.totalApplications,
         name='totalApplications'),
    path('jobs/<slug:job_slug>/applications/invite/', views.sendInvitation,
         name='sendInvitation'),
]
