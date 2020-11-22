from urllib import request

from django.conf.urls import url
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from .forms import RegisterForm
from .tokens import account_activation_token


class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = RegisterForm()
        return render(request,
                      'accounts/register.html',
                      {'form': form})

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Account activation.'
            message = render_to_string('accounts/email_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(
                request, 'Confirm your email address to complete registration.')
            form = RegisterForm()
            return render(request,
                          'accounts/register.html',
                          {'form': form})
        else:
            return render(request,
                          'accounts/register.html',
                          {'form': form})


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = AuthenticationForm()
        return render(request,
                      'accounts/login.html',
                      {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if not request.POST.get('remember'):
                request.session.set_expiry(0)
            if request.GET.get('next'):
                return redirect(request.GET['next'])
            else:
                return redirect('index')
        else:
            return render(request,
                          'accounts/login.html',
                          {'form': form})


class ForgotPasswordView(View):

    def get(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            # messages.error(request, 'Please correct the error below.')
            pass


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        message = ('Thank you for confirming your email address.'
                   '\nNow you can log in to your account.')
        return HttpResponse(message)
    else:
        message = 'The activation link is invalid!'
        return HttpResponse(message)


class PasswordChange(LoginRequiredMixin, View):

    def get(self, request):
        return render(request,
                      'accounts/password_change.html')

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return render(request,
                          'accounts/password_change.html')
        else:
            return render(request,
                          'accounts/password_change.html',
                          {'form': form})
