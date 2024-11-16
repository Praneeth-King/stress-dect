from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class UserAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs that don't require authentication
        public_urls = [
            reverse('index'),
            reverse('UserLogin'),
            reverse('AdminLogin'),
            reverse('UserRegister'),
            reverse('UserRegisterActions'),
            reverse('UserLoginCheck'),
            reverse('AdminLoginCheck'),
            reverse('logout'),
        ]
        
        # Check if the current URL is a user-specific URL
        is_user_url = request.path.startswith('/User') and request.path not in public_urls
        
        # If it's a user URL and user is not logged in, redirect to login
        if is_user_url and not request.session.get('loginid'):
            messages.error(request, 'Please login to access this page')
            return redirect('UserLogin')
            
        response = self.get_response(request)
        return response
