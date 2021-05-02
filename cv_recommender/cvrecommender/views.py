from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.paginator import Paginator
import datetime
from .forms import JobPostForm, EditJobForm, JobApplicationForm
from .models import Job, JobApplication
from custom_decorators.custom_decorator import allowed_users
from custom_scripts.custom_functions import sort_dict_and_return


# Create your views here.

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


@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
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


@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def currentOpeningJobs(request):
    opening_jobs = Job.published.filter(recruiter=request.user.recruiter)\
        .order_by('-publish')

    paginator = Paginator(opening_jobs, 3)
    page = request.GET.get('page')
    opening_jobs = paginator.get_page(page)
    return render(request, 'view_current_job.html', {'opening_jobs': opening_jobs})


@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def allJobs(request):
    all_jobs = Job.objects.filter(recruiter=request.user.recruiter)\
        .order_by('-publish')
    today = datetime.datetime.now()

    paginator = Paginator(all_jobs, 10)
    page = request.GET.get('page')
    all_jobs = paginator.get_page(page)

    return render(request, 'view_all_job.html', {'all_jobs': all_jobs, 'today': today})


def home(request):
    all_jobs = Job.objects.all()
    latest_jobs = Job.published.all().order_by('-publish')[:8]
    job_number = Job.published.all().count()

    sorted_cat_dict, sliced_dict, top_3 = sort_dict_and_return(all_jobs)

    context = {'job_number': job_number, 'latest_jobs': latest_jobs,
               'sliced_dict': sliced_dict, 'top_3': top_3}

    return render(request, 'index.html', context)


def allPublishedJobs(request, job_cat=None):
    if job_cat:
        all_jobs = Job.published.filter(
            job_category=job_cat).order_by('-publish')
    else:
        all_jobs = Job.published.all().order_by('-publish')

    paginator = Paginator(all_jobs, 12)
    page = request.GET.get('page')
    all_jobs = paginator.get_page(page)

    context = {'all_jobs': all_jobs}
    return render(request, 'job_layout.html', context)


def allCategories(request):
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    context = {'sorted_cat_dict': sorted_cat_dict}

    return render(request, 'all_categories.html', context)


# def jobCategory(request, job_cat):
#     all_jobs = Job.published.filter(job_category=job_cat).order_by('-publish')

#     paginator = Paginator(all_jobs, 12)
#     page = request.GET.get('page')
#     all_jobs = paginator.get_page(page)

#     context = {'all_jobs': all_jobs}
#     return render(request, 'job_layout.html', context)


def jobDetail(request, job_slug):
    job = get_object_or_404(Job, slug=job_slug)
    related_jobs = Job.published.filter(job_category=job.job_category)\
        .exclude(id=job.id).order_by('-publish')[:4]

    skill_bonus = []
    skill_req = job.skill_req.split(',')
    responsibility = job.responsibility.split('.')
    description = job.description.split('.')
    if job.skill_bonus:
        skill_bonus = job.skill_bonus.split(',')

    context = {'job': job, 'skill_req': skill_req,
               'skill_bonus': skill_bonus, 'responsibility': responsibility,
               'description': description, 'related_jobs': related_jobs}

    return render(request, 'job_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def apply(request, job_slug):
    job = get_object_or_404(Job, slug=job_slug)

    if request.method == 'POST':
        application_form = JobApplicationForm(data=request.POST,
                                              files=request.FILES)
        if application_form.is_valid():
            application_form_obj = application_form.save(commit=False)
            application_form_obj.applicant = request.user.applicant
            job.applicant.add(request.user.applicant)
            application_form_obj.save()
            job.save()
            messages.success(request, 'You application has\
                            submitted successfully')
            return redirect('editapplicantprofile')
        else:
            messages.error(request, 'Please input valid data')
            return render(request, 'apply.html', {'application_form': application_form})
    else:
        application_form = JobApplicationForm()

    return render(request, 'apply.html', {'application_form': application_form})
