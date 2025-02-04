# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import UserProfile  # Import the Profile model

def register(request):
    if request.method == 'POST':
        # Extract form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Validation (same as before)

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'register.html')


        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.save()

        # Create UserProfile and save additional details
        user_profile = UserProfile.objects.create(user=user, phone=phone, address=address)
        user_profile.save()

        # Log the user in after successful registration
        login(request, user)

        # Redirect to home or dashboard
        return redirect('home')

    return render(request, 'register.html')




def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Successful login
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
        else:
            # Invalid credentials
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Stay on the login page with an error message

    return render(request, 'login.html')


def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.user.is_authenticated:
        data = {
            "full_name": request.user.get_full_name(),
            "email": request.user.email,
            "phone": user_profile.phone,  # Example if you have a custom field
            "address": user_profile.address,  # Example if stored in a profile model
        }
    else:
        context = {}
    return render(request, 'shop/profile.html', data)