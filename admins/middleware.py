from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class AdminAuthMiddleware:
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
        
        # Check if the current URL is an admin-specific URL
        is_admin_url = request.path.startswith('/Admin') and request.path not in public_urls
        
        # If it's an admin URL and admin is not logged in, redirect to login
        if is_admin_url and not request.session.get('admin_logged_in'):
            messages.error(request, 'Please login as admin to access this page')
            return redirect('AdminLogin')
            
        response = self.get_response(request)
        return response
