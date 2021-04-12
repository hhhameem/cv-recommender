from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from custom_decorators.custom_decorator import allowed_users
from .forms import CreateUserForm, LoginUserForm, UserEditForm, ApplicantEditForm, RecruiterEditForm
from .models import Applicant, Recruiter
# Create your views here.


# @unauthenticated_user
def register(request):
    if request.method == 'POST':
        user_registration_form = CreateUserForm(request.POST)
        if user_registration_form.is_valid():
            user_type = user_registration_form.cleaned_data['user_type']

            new_user = user_registration_form.save(commit=False)
            new_user.set_password(
                user_registration_form.cleaned_data['password2'])
            new_user.save()

            if user_type == 'applicant':
                Applicant.objects.create(user=new_user)
            else:
                Recruiter.objects.create(user=new_user)

            group = Group.objects.get(name=user_type)
            new_user.groups.add(group)

            messages.success(request, 'Registration successfull for User Type: '
                             + user_type + 'and username ' + user_registration_form.cleaned_data['username'])
            return redirect('login')
    else:
        user_registration_form = CreateUserForm()

    return render(request, 'registration/signup.html', {'user_registration_form': user_registration_form})


# @unauthenticated_user
def userlogin(request):
    if request.method == 'POST':
        login_form = LoginUserForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
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

    return render(request, 'registration/login.html', {'login_form': login_form})


@login_required(login_url='login')
def userlogout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def applicantdashboard(request):
    return render(request, 'registration/applicant-dashboard.html')


@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def recruiterdashboard(request):
    return render(request, 'registration/applicant-dashboard.html')


@login_required(login_url='login')
@allowed_users(allowed_group=['applicant'])
def applicantEdit(request):
    pass


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

    return render(request, 'registration/recruiter_profile_edit.html',
                  {'user_form': user_form, 'recruiter_form': recruiter_form})


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

    return render(request, 'registration/applicant_profile_edit.html',
                  {'user_form': user_form, 'applicant_form': applicant_form})
