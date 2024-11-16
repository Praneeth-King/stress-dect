from django.shortcuts import render, redirect
from users.forms import UserRegistrationForm
from django.views.decorators.cache import never_cache

def index(request):
    return render(request, 'index.html', {})

@never_cache
def logout(request):
    # Clear all session data
    request.session.flush()
    response = redirect('index')
    # Add cache control headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def UserLogin(request):
    return render(request, 'UserLogin.html', {})

def AdminLogin(request):
    return render(request, 'AdminLogin.html', {})


def UserRegister(request):
    form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})
