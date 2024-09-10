from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def login_user(request):
    # user = None
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('login-user')
    else:
        return render(request, 'authenticate/login.html')
    
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')
        