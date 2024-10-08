from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.shortcuts import render, redirect
from django.contrib import messages
from string import ascii_letters, ascii_lowercase

# Create your views here.
def user_login(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            user = None

        if user and user.check_password(raw_password=password):
            login(request, user)
            messages.success(request, f'You are welcome, {request.user.username}!')
            return redirect('/')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request,
                  template_name="app_user/login.html")

def user_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not username:
            messages.error(request, 'Username cannot be empty !!!')
            return redirect('/users/login/')

        user_exists = len(User.objects.filter(username=username))

        if not user_exists:
            if (password1 == password2) and len(password1) > 8:
                user = User.objects.create(
                    username=username
                )
                user.set_password(raw_password=password1)
                user.save()
                messages.success(request, f'Your account has been created!')
                return redirect('/users/login/')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('/users/registration/')
    else:
            messages.error(request, 'Username is already taken')
            return redirect('/users/registration/')
    return render(request,
                  template_name="app_user/registration.html")

def user_logout(request):
    messages.info(request, f'You are now logged out')
    logout(request)
    return redirect('/users/login/')