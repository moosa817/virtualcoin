# views.py
from django.http import HttpResponse
from django.conf import settings
from .models import CustomUser
from .crypto_utils import (
    generate_rsa_keypair,
    sign_data,
)  # Assuming this function generates RSA key pair
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import CustomUser, Transaction, Block
from .transactions import make_transaction, get_balance
from django.db.models import Q


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username").lower()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # Redirect to initial setup page
            return redirect("initial_setup")

    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


@login_required
def initial_setup(request):
    if request.user.is_new_user_setup_completed:
        return redirect("home")

    if request.method == "POST":
        private_key, public_key = generate_rsa_keypair()

        user = request.user

        user.public_key = public_key.strip()
        user.is_new_user_setup_completed = True
        user.save()
        # initial balance

        make_transaction(
            "system", request.user.username, 1000, settings.SYSTEM_PRIVATE_KEY
        )

        # Save private key to a file and serve it for download
        response = HttpResponse(private_key, content_type="text/plain")
        response["Content-Disposition"] = 'attachment; filename="private_key.pem"'
        return response

    return render(request, "setup.html", {})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required(login_url="/login/")
def home(request):
    balance = get_balance(request.user)

    if not request.user.is_new_user_setup_completed:
        return redirect("initial_setup")

    return render(request, "index.html", {"balance": balance})


@login_required(login_url="/login/")
def make_transaction_view(request):
    if request.method == "POST":
        sender = request.user.username
        recipient = request.POST.get("recipient")
        amount = request.POST.get("amount")

        # Handle private key file upload
        private_key_file = request.FILES.get("privateKeyFile")
        if private_key_file:
            private_key = private_key_file.read().decode(
                "utf-8"
            )  # Read and decode the private key file content

        response = make_transaction(sender, recipient, amount, private_key)

        try:
            receiver_user = CustomUser.objects.get(
                Q(username=recipient)
                | Q(public_key=recipient.strip().replace("\r\n", "\n"))
            )
        except:
            receiver_user = None

        if response == "Transaction Successful" and receiver_user:
            messages.success(
                request, f"Sent {amount} Coins to {receiver_user} successfully"
            )
        else:
            messages.error(request, response)

        return redirect(
            "home"
        )  # Redirect to dashboard or appropriate view after transaction

    return redirect("home")


@login_required(login_url="/login/")
def blockchain_view(request):
    blocks = Block.objects.all().order_by("index")
    return render(request, "blockchain.html", {"blocks": blocks})
