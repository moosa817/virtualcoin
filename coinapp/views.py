from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("home")  # Change 'home' to your desired redirect URL
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Change 'home' to your desired redirect URL
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


def Logout(request):
    logout(request)
    return redirect("home")


@login_required(login_url="/login/")
def home(request):
    return render(request, "index.html", {})


@login_required(login_url="/login/")
def blockchain(request):
    return render(request, "blockchain.html", {})
