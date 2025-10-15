from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from .forms import SignUpForm, LoginForm
import os


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return render(request, 'users/logout.html')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


def emergency_password_reset(request):
    """
    Emergency password reset endpoint for when you're locked out.
    Requires EMERGENCY_SECRET environment variable for security.
    
    Usage: /users/emergency/?secret=YOUR_SECRET&username=admin&password=newpass123
    
    IMPORTANT: This is a backup solution. Remove or disable after use!
    """
    # Security check - require secret key
    secret = request.GET.get('secret', '')
    expected_secret = os.environ.get('EMERGENCY_SECRET', '')
    
    if not expected_secret:
        return HttpResponse(
            '❌ EMERGENCY_SECRET not configured in environment variables.',
            status=500
        )
    
    if secret != expected_secret:
        return HttpResponse('❌ Unauthorized - Invalid secret key', status=403)
    
    # Get parameters
    username = request.GET.get('username')
    new_password = request.GET.get('password')
    email = request.GET.get('email', 'admin@example.com')
    
    if not username or not new_password:
        return HttpResponse(
            '❌ Missing required parameters: username and password',
            status=400
        )
    
    try:
        # Check if user exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.is_staff = True
            user.is_superuser = True
            user.email = email
            user.save()
            return HttpResponse(
                f'✅ SUCCESS! Password reset for user: {username}<br><br>'
                f'You can now login at <a href="/admin/">/admin/</a><br><br>'
                f'<strong>IMPORTANT:</strong> For security, disable this endpoint after use!',
                content_type='text/html'
            )
        else:
            # Create new superuser
            user = User.objects.create_superuser(username, email, new_password)
            return HttpResponse(
                f'✅ SUCCESS! Superuser created: {username}<br><br>'
                f'You can now login at <a href="/admin/">/admin/</a><br><br>'
                f'<strong>IMPORTANT:</strong> For security, disable this endpoint after use!',
                content_type='text/html'
            )
    except Exception as e:
        return HttpResponse(
            f'❌ Error: {str(e)}',
            status=500
        )
