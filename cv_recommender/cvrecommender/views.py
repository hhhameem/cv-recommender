from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.core.paginator import Paginator
import datetime
from .forms import JobPostForm, EditJobForm, JobApplicationForm
from .models import Job, JobApplication
from custom_decorators.custom_decorator import allowed_users
from custom_scripts.custom_functions import sort_dict_and_return, convert_to_list
from custom_scripts.scoring import score_of_an_applicant
from custom_scripts.send_invitation_mail import send_mail_to_selected_candidate

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
        .order_by('-publish', '-status')
    today = datetime.datetime.now()

    paginator = Paginator(all_jobs, 10)
    page = request.GET.get('page')
    all_jobs = paginator.get_page(page)

    return render(request, 'view_all_job.html', {'all_jobs': all_jobs, 'today': today})


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
    return render(request, 'all_applicants_per_job.html', {'myjob': myjob, 'candidates': candidates, 'total_candidates': total_candidates, 'mail_sent': mail_sent})


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

    send_mail_to_selected_candidate(myjob, candidates)
    messages.success(request,
                     'E-Mail sent successfully to the selected candidates')
    mail_sent = True
    return render(request, 'all_applicants_per_job.html', {'myjob': myjob, 'candidates': candidates, 'total_candidates': total_candidates, 'mail_sent': mail_sent})


def home(request):
    latest_jobs = Job.published.all().order_by('-publish')[:8]
    job_number = Job.published.all().count()

    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())

    context = {'job_number': job_number, 'latest_jobs': latest_jobs,
               'sliced_dict': sliced_dict, 'top_3': top_3,
               'sorted_cat_dict': sorted_cat_dict}

    return render(request, 'index.html', context)


@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
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


@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
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

    context = {'job': job, 'skill_req': skill_req,
               'skill_bonus': skill_bonus, 'responsibility': responsibility,
               'description': description, 'related_jobs': related_jobs, 'applied': applied}

    return render(request, 'job_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def apply(request, job_slug):
    job_list = []
    application_list = []
    job = get_object_or_404(Job, slug=job_slug)
    job_list.append(convert_to_list(job.skill_req))
    job_list.append(convert_to_list(job.skill_bonus))
    job_list.append(convert_to_list(job.min_education))
    job_list.append(float(job.cgpa))
    job_list.append(job.experience)

    print('This is JOB: ', job_list)

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

            print('This is Application: ', application_list)
            application_form_obj.score = score_of_an_applicant(
                job_list, application_list)
            application_form_obj.save()
            job.save()
            messages.success(request, 'You application has\
                            submitted successfully')
            return redirect('applicantdashboard')
        else:
            messages.error(request, 'Please input valid data')
            return render(request, 'apply.html', {'application_form': application_form,
                                                  'job': job})
    else:
        application_form = JobApplicationForm()

    return render(request, 'apply.html', {'application_form': application_form,
                                          'job': job})


@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def allappliedjobs(request):
    applied_jobs = JobApplication.objects.filter(
        applicant=request.user.applicant).order_by('apply_time')

    paginator = Paginator(applied_jobs, 3)
    page = request.GET.get('page')
    applied_jobs = paginator.get_page(page)

    return render(request, 'applied_job_list.html', {'applied_jobs': applied_jobs})
