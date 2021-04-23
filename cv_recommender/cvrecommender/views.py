from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from custom_decorators.custom_decorator import allowed_users
from .forms import JobPostForm, EditJobForm
from .models import Job
import datetime


# Create your views here.

def home(request):
    return render(request, 'index.html')


@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def postJob(request):
    if request.method == 'POST':
        job_form = JobPostForm(data=request.POST, files=request.FILES)
        if job_form.is_valid():
            job_form_obj = job_form.save(commit=False)
            job_form_obj.recruiter = request.user.recruiter
            job_form_obj.save()
            messages.success(request, 'Job Has Successfully Posted.')
            return redirect('recruiterdashboard')
        else:
            return render(request, 'add_job.html', {'job_form': job_form})
    else:
        job_form = JobPostForm()

    return render(request, 'add_job.html')


def editjob(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        jobEditForm = EditJobForm(instance=job, data=request.POST)
        if jobEditForm.is_valid():
            jobEditForm.save()
            messages.success(request, 'You Job has been \
                            successfully edited and saved')
            return redirect('recruiterdashboard')
    else:
        jobEditForm = EditJobForm(instance=job)

    return render(request, 'edit_job.html', {'jobEditForm': jobEditForm, 'job': job})


def currentOpeningJobs(request):
    opening_jobs = Job.published.all()
    # print(opening_jobs)
    return render(request, 'view_current_job.html', {'opening_jobs': opening_jobs})


def allJobs(request):
    all_jobs = Job.objects.all()
    today = datetime.datetime.now()
    # print(opening_jobs)
    return render(request, 'view_all_job.html', {'all_jobs': all_jobs, 'today': today})


def jobDetail(request, job_slug):
    pass
