from django.shortcuts import render, redirect

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import login as login, logout

from . import forms
from django.conf import settings

def password_reset_request(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    
    if request.method == "POST":
        form = forms.PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                current_site = get_current_site(request)
                reset_url = f'http://{current_site.domain}{reverse_lazy("password_reset:confirm", kwargs={"uidb64": uid, "token": token})}'

                email_subject = 'Password Reset - Talent Hunt'
                email_message = render_to_string('password_reset/email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })

                email_to_be_sent = EmailMessage(
                    email_subject,
                    email_message,
                    settings.EMAIL_HOST_USER,
                    [email],  
                )
                email_to_be_sent.content_subtype = 'html'
                email_to_be_sent.send()

                return render(request, 'password_reset/sent.html')

            else:
                return redirect('password_reset:request')
        
    else:
        form = forms.PasswordResetForm()

    return render(request, 'password_reset/request.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = forms.CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset:done')
        else:
            form = forms.CustomSetPasswordForm(user)

        return render(request, 'password_reset/confirm.html', {'form': form})
    
    else:
        return render(request, 'password_reset/invalid.html')

    
def password_reset_sent(request):
    if request.user.is_authenticated:
        redirect('main:home')
    return render(request, 'password_reset/sent.html')


def password_reset_done(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'password_reset/done.html')


def password_reset_invalid(request):
    return render(request, 'password_reset/invalid.html')

        