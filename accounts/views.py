from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    #checks to see if you are doing a post request on the register page
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #validations!!!!
        #do passwords match
        if password == password2:
            #is the user name you requested already taken
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That user already exists')
                return redirect('register')
            else:
                # is the email taken
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email user already exists')
                    return redirect('register')
                else:
                    #passed validations, create the user in the database
                    user = User.objects.create_user(
                        first_name = first_name,
                        last_name = last_name,
                        username = username,
                        email = email,
                        password = password
                    )
                    # if you want to login the new user automatically
                    # auth.login(request, user)
                    # messages.success(request, 'you are now logged in!')
                    # return redirect('index')
                    #OR if you want to just save the user info and take them to the login page
                    user.save()
                    messages.success(request, 'you are now registered and can now log in!')
                    return redirect('login')


        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')

def login(request):
     #checks to see if you are doing a post request on the login page
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        #passes info to authenticate and login
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            messages.success(request, "You are now logged in")
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')
