from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.core.paginator import Paginator
import datetime
from .forms import JobPostForm, EditJobForm, JobApplicationForm, SearchForm
from .models import Job, JobApplication
from custom_decorators.custom_decorator import allowed_users
from custom_scripts.custom_functions import sort_dict_and_return, convert_to_list
from custom_scripts.scoring import score_of_an_applicant
from custom_scripts.send_invitation_mail import send_mail_to_selected_candidate


# Create your views here.

# view for posting jobs
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
            context = {'job_form': job_form}
            return render(request, 'add_job.html', context)
    else:
        job_form = JobPostForm()
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    context = {'sliced_dict': sliced_dict, 'job_form': job_form}

    return render(request, 'add_job.html', context)


# view for editing jobs
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
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    context = {'jobEditForm': jobEditForm, 'job': job,
               'sliced_dict': sliced_dict}

    return render(request, 'edit_job.html', context)


# view for showing currently opening jobs of a specific recruiter
@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def currentOpeningJobs(request):
    opening_jobs = Job.published.filter(recruiter=request.user.recruiter)\
        .order_by('-publish')
    paginator = Paginator(opening_jobs, 3)
    page = request.GET.get('page')
    opening_jobs = paginator.get_page(page)
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    context = {'opening_jobs': opening_jobs, 'sliced_dict': sliced_dict}

    return render(request, 'view_current_job.html', context)


# view for showing all jobs posted by a specific recruiter
@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def allJobs(request):
    all_jobs = Job.objects.filter(recruiter=request.user.recruiter)\
        .order_by('-publish', '-status')
    today = datetime.datetime.now()
    paginator = Paginator(all_jobs, 10)
    page = request.GET.get('page')
    all_jobs = paginator.get_page(page)
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    context = {'all_jobs': all_jobs, 'today': today,
               'sliced_dict': sliced_dict}

    return render(request, 'view_all_job.html', context)


# view for showing all applications submitted to a specific job
@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def totalApplications(request, job_slug):
    myjob = get_object_or_404(Job, slug=job_slug)
    candidates = JobApplication.objects.filter(
        job=myjob.id).order_by('-score', '-related_experience_application',
                               '-total_experience_application', '-cgpa_application')
    total_candidates = candidates.count()
    paginator = Paginator(candidates, 15)
    page = request.GET.get('page')
    candidates = paginator.get_page(page)
    mail_sent = False
    context = {'myjob': myjob, 'candidates': candidates,
               'total_candidates': total_candidates, 'mail_sent': mail_sent}

    return render(request, 'all_applicants_per_job.html', context)


# view for sending invitation to the first 15 highest scorer
@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def sendInvitation(request, job_slug):
    myjob = get_object_or_404(Job, slug=job_slug)
    candidates = JobApplication.objects.filter(
        job=myjob.id).order_by('-score', '-related_experience_application',
                               '-total_experience_application', '-cgpa_application')[:14]
    total_candidates = candidates.count()
    paginator = Paginator(candidates, 15)
    page = request.GET.get('page')
    candidates = paginator.get_page(page)
    # function calling for sending mail
    send_mail_to_selected_candidate(myjob, candidates)
    messages.success(request,
                     'E-Mail sent successfully to the selected candidates')
    mail_sent = True
    context = {'myjob': myjob, 'candidates': candidates,
               'total_candidates': total_candidates, 'mail_sent': mail_sent}

    return render(request, 'all_applicants_per_job.html', context)


# view for showing all applied jobs to the applicant
@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def allappliedjobs(request):
    applied_jobs = JobApplication.objects.filter(
        applicant=request.user.applicant).order_by('apply_time')
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    paginator = Paginator(applied_jobs, 3)
    page = request.GET.get('page')
    applied_jobs = paginator.get_page(page)
    context = {'applied_jobs': applied_jobs, 'sliced_dict': sliced_dict}

    return render(request, 'applied_job_list.html', context)


# home view or landing page view
def home(request):
    latest_jobs = Job.published.all().order_by('-publish')[:8]
    job_number = Job.published.all().count()
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    searched_query = SearchForm()
    context = {'job_number': job_number, 'latest_jobs': latest_jobs,
               'sliced_dict': sliced_dict, 'top_3': top_3,
               'sorted_cat_dict': sorted_cat_dict, 'searched_query': searched_query}

    return render(request, 'index.html', context)


# view for search
@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def search(request):
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    if request.method == 'POST':
        searched_query = request.POST['searchquery']
        if searched_query:
            all_jobs = Job.published.filter(title__icontains=searched_query)
            paginator = Paginator(all_jobs, 12)
            page = request.GET.get('page')
            all_jobs = paginator.get_page(page)
        else:
            all_jobs = []
        context = {'searched_query': searched_query, 'all_jobs': all_jobs,
                   'sorted_cat_dict': sorted_cat_dict}

        return render(request, 'search_result.html', context)
    else:
        search_form = SearchForm()
    context = {'search_form': search_form, 'sorted_cat_dict': sorted_cat_dict}

    return render(request, 'search_result.html', context)


# view for showing published jobs
@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def allPublishedJobs(request, job_cat=None):
    if job_cat:
        all_jobs = Job.published.filter(
            job_category=job_cat).order_by('-publish')
        category = True
    else:
        all_jobs = Job.published.all().order_by('-publish')
        category = False
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    paginator = Paginator(all_jobs, 12)
    page = request.GET.get('page')
    all_jobs = paginator.get_page(page)
    context = {'all_jobs': all_jobs, 'sliced_dict': sliced_dict, 'top_3': top_3,
               'sorted_cat_dict': sorted_cat_dict, 'category': category}

    return render(request, 'job_layout.html', context)


# view for showing all category
@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def allCategories(request):
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    context = {'sliced_dict': sliced_dict, 'top_3': top_3,
               'sorted_cat_dict': sorted_cat_dict, }

    return render(request, 'all_categories.html', context)


# view for showing job details
@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def jobDetail(request, job_slug):
    job = get_object_or_404(Job, slug=job_slug)
    related_jobs = Job.published.filter(job_category=job.job_category)\
        .exclude(id=job.id).order_by('-publish')[:4]
    applied = False
    applicants = Job.objects.values_list(
        'applicant', flat=True).filter(slug=job_slug)
    if request.user.applicant.pk in applicants:
        applied = True
    skill_bonus = []
    skill_req = job.skill_req.split(',')
    responsibility = job.responsibility.split('.')
    description = job.description.split('.')
    if job.skill_bonus:
        skill_bonus = job.skill_bonus.split(',')
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    context = {'job': job, 'skill_req': skill_req,
               'skill_bonus': skill_bonus, 'responsibility': responsibility,
               'description': description, 'related_jobs': related_jobs, 'applied': applied,
               'sliced_dict': sliced_dict, 'sorted_cat_dict': sorted_cat_dict}

    return render(request, 'job_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def apply(request, job_slug):
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    job_list = []
    application_list = []
    job = get_object_or_404(Job, slug=job_slug)
    job_list.append(convert_to_list(job.skill_req))
    job_list.append(convert_to_list(job.skill_bonus))
    job_list.append(convert_to_list(job.min_education))
    job_list.append(float(job.cgpa))
    job_list.append(job.experience)
    if request.method == 'POST':
        application_form = JobApplicationForm(data=request.POST,
                                              files=request.FILES)
        if application_form.is_valid():
            application_form_obj = application_form.save(commit=False)
            application_form_obj.applicant = request.user.applicant
            application_form_obj.job = job
            job.applicant.add(request.user.applicant)
            application_list.append(convert_to_list(
                application_form_obj.skill_req_application))
            application_list.append(convert_to_list(
                application_form_obj.skill_bonus_application))
            application_list.append(convert_to_list(
                application_form_obj.education_application))
            application_list.append(
                float(application_form_obj.cgpa_application))
            application_list.append(
                application_form_obj.related_experience_application)
            application_form_obj.score = score_of_an_applicant(
                job_list, application_list)
            application_form_obj.save()
            job.save()
            messages.success(request, 'You application has\
                            submitted successfully')
            return redirect('applicantdashboard')
        else:
            messages.error(request, 'Please input valid data')
            context = {'application_form': application_form,
                       'job': job, 'sorted_cat_dict': sorted_cat_dict,
                       'sliced_dict': sliced_dict}
            return render(request, 'apply.html', context)
    else:
        application_form = JobApplicationForm()
    context = {'application_form': application_form,
               'job': job, 'sorted_cat_dict': sorted_cat_dict,
               'sliced_dict': sliced_dict}

    return render(request, 'apply.html', context)
