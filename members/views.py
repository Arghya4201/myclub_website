from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm



def login_user(request):
    # user = None
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in!', extra_tags='success')
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect',extra_tags='danger')
            return redirect('login-user')
    else:
        return render(request, 'authenticate/login.html')
    
def logout_user(request):
    logout(request)
    messages.error(request, 'You have been logged out!', extra_tags='danger')
    return redirect('home')

def register_user(request):
    # form  = RegisterUserForm()
    if request.method == 'POST':
        form =  RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered', extra_tags='success')
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {'form': form})
        