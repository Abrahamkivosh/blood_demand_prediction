# middleware to check if user is authenticated or not and redirect to login page if not authenticated
#  if authenticated then redirect to  intended url

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class Authenticated(MiddlewareMixin):
    def process_request(self, request):
        excluded_urls = [reverse('forecast:login'), reverse('forecast:index'), 
                         reverse('forecast:password_reset'), 
                         reverse('forecast:password_reset_request'), 
                        reverse('forecast:password_reset_confirm'),
                         ]
        
        # Check if the requested URL is in the excluded list
        if not request.user.is_authenticated and request.path not in excluded_urls:
            # Redirect unauthenticated users to the login page
            return redirect(reverse('forecast:login'))
        return None
    
