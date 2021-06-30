from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from .forms import CreateUserForm, LoginUserForm, UserEditForm, ApplicantEditForm, RecruiterEditForm
from .models import Applicant, Recruiter
from cvrecommender.models import Job, JobApplication
from custom_decorators.custom_decorator import allowed_users
from custom_scripts.custom_functions import sort_dict_and_return, convert_to_list

# Create your views here.


# view for registering new user
def register(request):
    if request.method == 'POST':
        user_registration_form = CreateUserForm(request.POST)
        if user_registration_form.is_valid():
            user_type = user_registration_form.cleaned_data['user_type']

            new_user = user_registration_form.save(commit=False)
            new_user.set_password(
                user_registration_form.cleaned_data['password2'])  # set password by hashing
            new_user.save()
            # create instance of new user in the appropriate model
            if user_type == 'applicant':
                Applicant.objects.create(user=new_user)
            else:
                Recruiter.objects.create(user=new_user)
            # get the group if exists, otherwise create and add user to that group
            group, created = Group.objects.get_or_create(name=user_type)
            new_user.groups.add(group)

            messages.success(request, 'Registration successfull for User Type: '
                             + user_type + ' and username ' + user_registration_form.cleaned_data['username'])
            return redirect('login')
    else:
        user_registration_form = CreateUserForm()
    context = {'user_registration_form': user_registration_form}

    return render(request, 'registration/signup.html', context)


# view fro logging in existing user
def userlogin(request):
    if request.method == 'POST':
        login_form = LoginUserForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.groups.filter(name='applicant').exists():
                        return redirect('applicantdashboard')
                    else:
                        return redirect('recruiterdashboard')
                else:
                    return HttpResponse("Disabled Account")
            else:
                messages.error(request, 'Username or Password Incorrect')
        else:
            messages.error(request, 'Username or Password Incorrect')
    else:
        login_form = LoginUserForm()
    context = {'login_form': login_form}

    return render(request, 'registration/login.html', context)


@login_required(login_url='login')
def userlogout(request):
    logout(request)
    return redirect('login')


# applicant dashboard view
@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def applicantdashboard(request):
    applied = JobApplication.objects.filter(applicant=request.user.applicant)
    if applied:
        total = applied.count()
        latest = applied.latest('apply_time')
    else:
        total = 0
        latest = None
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    context = {'total': total, 'latest': latest, 'sliced_dict': sliced_dict}

    return render(request, 'registration/applicant-dashboard.html', context)


# recruiter dashboard view
@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def recruiterdashboard(request):
    my_all_jobs = Job.objects.filter(recruiter=request.user.recruiter)
    total = my_all_jobs.count()
    current = Job.published.filter(recruiter=request.user.recruiter).count()
    if total > 0:
        last_published = my_all_jobs.latest('publish')
        last_edited = my_all_jobs.latest('last_modified')
    else:
        last_published = date.today()
        last_edited = date.today()
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    context = {'total': total, 'current': current, 'sliced_dict': sliced_dict,
               'last_edited': last_edited, 'last_published': last_published}

    return render(request, 'registration/recruiter_dashboard.html', context)


# view for editing recruiter profile
@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def recruiteredit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        recruiter_form = RecruiterEditForm(instance=request.user.recruiter,
                                           data=request.POST, files=request.FILES)
        if user_form.is_valid() and recruiter_form.is_valid():
            user_form.save()
            recruiter_form.save()
        else:
            messages.error(request, 'Data is not Valid')
    else:
        user_form = UserEditForm(instance=request.user)
        recruiter_form = RecruiterEditForm(instance=request.user.recruiter)
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    context = {'user_form': user_form, 'recruiter_form': recruiter_form,
               'sliced_dict': sliced_dict}

    return render(request, 'registration/recruiter_profile_edit.html', context)


# view for editing applicant profile
@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def applicantedit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        applicant_form = ApplicantEditForm(instance=request.user.applicant,
                                           data=request.POST, files=request.FILES)
        if user_form.is_valid() and applicant_form.is_valid():
            user_form.save()
            applicant_form.save()
        else:
            messages.error(request, 'Data is not Valid')
    else:
        user_form = UserEditForm(instance=request.user)
        applicant_form = ApplicantEditForm(instance=request.user.applicant)
    sorted_cat_dict, sliced_dict, top_3 = \
        sort_dict_and_return(Job.objects.all())
    context = {'user_form': user_form, 'applicant_form': applicant_form,
               'sliced_dict': sliced_dict}

    return render(request, 'registration/applicant_profile_edit.html', context)


def handler400(request, exception, template_name='400.html'):
    return render(request, template_name)


def handler403(request, exception, template_name='403.html'):
    return render(request, template_name)


def handler404(request, exception, template_name='404.html'):
    return render(request, template_name)


def handler500(request, template_name='500.html'):
    return render(request, template_name)
