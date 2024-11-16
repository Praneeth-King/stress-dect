from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def user_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('loginid'):
            messages.error(request, 'Please login to access this page')
            return redirect('UserLogin')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_logged_in'):
            messages.error(request, 'Please login as admin to access this page')
            return redirect('AdminLogin')
        return view_func(request, *args, **kwargs)
    return wrapper
