from django.http import HttpResponse
from django.shortcuts import render


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'base/403_forbidden.html')

    return wrapper_function
