# views.py

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth import get_user_model
from django.db.models import  Q
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm

UserModel = get_user_model()

def password_reset_index(request):
    return render(request, 'auth/password_reset_index.html')

def password_reset_request(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        try:
            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        except User.DoesNotExist:
            user = None
        if user:
            
            subject = 'Password Reset Request'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            message = render_to_string('emails/password_reset_email.html', {
                'user': user,
                'reset_url':  request.build_absolute_uri('/reset?uidb64=' + uid + '&token=' + token),
            })

            send_mail(
                subject=subject,
                html_message=message,
                message=message,
                from_email= 'hello@test.com',
                recipient_list=[user.email],
                fail_silently=False
                  )
            messages.success(request, 'An email has been sent to ' + user.email + ". Please check its inbox to continue resetting password.")
        else:
            messages.error(request, 'User does not exist.', extra_tags='danger')
        return redirect('forecast:password_reset')
    

    return redirect('forecast:password_reset')



def password_reset_confirm(request):
    try:
        passed_uidb64 = request.GET['uidb64']
        passed_token = request.GET['token']
        uid = force_str(urlsafe_base64_decode(passed_uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, passed_token):
        if request.method == 'POST':
                password = request.POST['password']
                password_confirm = request.POST['password_confirm']
                if password != password_confirm:
                    messages.error(request, 'Passwords do not match.', extra_tags='danger')
                    return redirect('forecast:password_reset_confirm' + '?uidb64=' + passed_uidb64  )
                else:
                    user.set_password(password)
                    user.save()
                    # Display a success message or redirect to a confirmation page.
                    messages.success(request, 'Password successfully reset. You can now log in with the new credentials.')
                    return redirect('forecast:login')
        else:
            url = request.build_absolute_uri('/reset?uidb64=' + passed_uidb64 + '&token=' + passed_token)

        return render(request, 'auth/password_reset_confirm.html', {'url': url, 'user': user})
    else:
        # Handle invalid token or user not found.
        # Display an error message or redirect to an error page.
        messages.error(request, 'The reset password link is no longer valid.', extra_tags='danger')
        return redirect('forecast:login')