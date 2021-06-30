from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

# def unauthenticated_user(view_function):
#     def wrapper_function(request, *args, **kwargs):
#         group = None
#         if request.user.is_authenticated:
#             print("user authenticated")
#             if request.user.groups.exists():
#                 print("inside if")
#                 group = request.user.groups.all()[0].name
#                 print('group:', group)
#             print('group1:', group)
#             if group == 'applicant':
#                 return redirect('applicantdashboard')
#             if group == 'recruiter':
#                 return redirect('recruiterdashboard')
#         else:
#             return view_function(request, *args, **kwargs)

#     return wrapper_function


# decorator for access persmission group wise
def allowed_users(allowed_group=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group in allowed_group:
                    return view_function(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            else:
                return redirect('login')
        return wrapper_function
    return decorator
