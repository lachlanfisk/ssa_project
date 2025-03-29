from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, TopUpForm
import requests
from django.conf import settings
from django.contrib.auth.models import User
from .models import Transaction

def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your account has been created! You can now log in.")
                return redirect('users:login')
        return render(request, 'users/register.html', {'form': form})
    else:
        return redirect('/users')

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            recaptcha_response = request.POST.get("recaptcha-token")  # Updated
            # Verify reCAPTCHA
            data = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response,
                'remoteip': request.META.get('REMOTE_ADDR'),
            }
            recaptcha_verification = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data=data
            )
            result = recaptcha_verification.json()
            # Check reCAPTCHA response
            if not result.get("success"):
                messages.error(request, "reCAPTCHA validation failed. Please try again.")
                return redirect("users:login")  # Redirect back to the login page
            # Authenticate user if reCAPTCHA is valid
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the next URL if provided, else default to user profile
                next_url = request.GET.get('next', reverse("users:user"))  # Simplified fallback
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        return render(request, "users/login.html")
    else:
        return redirect("/users")

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('users:login')

def user_view(request):
    profile = request.user.profile  # Get the logged-in user's profile
    return render(request, 'users/user.html', {'balance': profile.balance})

def user(request):
    profile = request.user.profile
    return render(request, 'users/user.html', {
        'user': request.user,
        'balance': profile.balance
    })

@login_required
def top_up(request):
    profile = request.user.profile
    if request.method == "POST":
        form = TopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            profile.balance += amount
            profile.save()
            Transaction.objects.create(user=request.user, amount=amount)
            messages.success(request, f"Your balance has been updated by ${amount}")
            return redirect('users:user')
        else:
            return render(request, 'users/top_up.html', {'form': form})
    else:
        form = TopUpForm()
        return render(request, 'users/top_up.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == "POST":
        password = request.POST.get('password')
        user = request.user
        
        # Authenticate password before proceeding with deletion
        user = authenticate(username=user.username, password=password)
        
        if user is not None:
            request.user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            return redirect('users/user')
        else:
            messages.error(request, "Incorrect password. Please try again.")
    return render(request, 'users/delete_account.html')