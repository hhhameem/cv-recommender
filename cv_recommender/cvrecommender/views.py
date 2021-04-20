from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm
# Create your views here.


def home(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def postJob(request):
    if request.method == 'POST':
        job_form = JobPostForm(data=request.POST, files=request.FILES)
        if job_form.is_valid():
            job_form_obj = job_form.save(commit=False)
            job_form_obj.recruiter = request.user.recruiter
            print(request.user.recruiter)
            job_form_obj.save()
            return redirect('recruiterdashboard')
        else:
            return render(request, 'add_job.html', {'job_form': job_form})
    else:
        job_form = JobPostForm()

    return render(request, 'add_job.html')
