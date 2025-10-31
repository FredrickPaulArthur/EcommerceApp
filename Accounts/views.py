from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings



def dashboard(request):
    return render(request, "Accounts/dashboard.html")



def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("Products:product_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'Accounts/register.html', context)



def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("Accounts:dashboard")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login details.")
    else:
        form = CustomAuthenticationForm()

    return render(request, "Accounts/login.html", {'form': form})



@login_required
def logout_view(request):
    logout(request)
    return redirect('Accounts:dashboard')



def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = CustomUser.objects.filter(email=email)
            if users.exists():
                for user in users:
                    subject = "Password Reset Requested"
                    email_template_name = "Accounts/password_reset_email.txt"
                    context = {
                        "email": user.email,
                        "domain": request.get_host(),
                        "site_name": "EcommerceApp",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "https" if request.is_secure() else "http",
                    }
                    email_body = render_to_string(email_template_name, context)
                    send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

                messages.success(request, "We've emailed you instructions for resetting your password.")
                return redirect("Accounts:password_reset_sent")
            else:
                messages.error(request, "No user found with that email address.")
    else:
        form = PasswordResetForm()

    return render(request, "Accounts/password_reset_form.html", {"form": form})



def password_reset_sent(request):
    return render(request, "Accounts/password_reset_sent.html")



@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # ✅ keeps user logged in
            messages.success(request, "Your password has been changed successfully!")
            return redirect("Accounts:password_change_done")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "Accounts/password_change_form.html", {"form": form})



def password_change_done(request):
    return render(request, "Accounts/password_change_done.html")



def password_reset_confirm(request, uidb64, token):
    return render(request, "Accounts/password_reset_confirm.html")



def password_reset_complete(request):
    return render(request, "Accounts/password_reset_complete.html")