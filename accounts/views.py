from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import RegistrationForm,LoginForm
from django.contrib.auth.decorators import login_required

# User Registration view
def register_view(request):
    if request.user.is_authenticated:
        return redirect('shortener:dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,f'Welcome {user.username}! Your account has been created successfully.')
            return redirect('shortener:dashboard')
        else:
            messages.error(request,'Please fix the error below')

    else:
        form = RegistrationForm()    

    return render(request,'accounts/register.html',{'form':form})

# User Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('shortener:dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # Redirect to 'next' param if present, else dashboard
            next_url = request.GET.get('next', 'shortener:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm(request)

    return render(request, 'accounts/login.html', {'form': form})

# User Logout view
def logout_view(request):
    logout(request)
    messages.info(request,'You have been logged out successfully!')
    return redirect('accounts:login')    