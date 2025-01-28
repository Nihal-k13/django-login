
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.


def index(request):
    return render(request,'registration/index.html')

@login_required()
def home(request):
    return render(request, 'registration/home.html')



def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! please try some other username")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request,"username already registered")
            return redirect('signup')
        if pass1 != pass2:
            messages.error(request,"password didn't match!")
            return redirect('signup')  
        else:  
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request,"your account has been successfully created.")
            return redirect('signin')
    return render(request, 'registration/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        User = authenticate(username=username, password=pass1)

        if User is not None:
            login(request,User)
            fname = User.first_name
            return render(request,'registration/home.html',{'fname':fname})
        else:
            messages.error(request,"invalid username and password!")
            return redirect('signin')
    return render(request,'registration/signin.html')
def signout(request):
    logout(request)
    messages.success(request, "logged out successfully!")
    return redirect('signin')