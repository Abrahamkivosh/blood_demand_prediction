# middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages

class RedirectAuthenticatedUser(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.path == reverse('forecast:login'):
            # Redirect authenticated users away from the login page
            messages.warning(request, 'You are already logged in.', extra_tags='warning')
            return redirect('forecast:dashboard') 
        return None
