from .models import Transaction, CustomUser
from .crypto_utils import sign_data, verify_signature
from django.shortcuts import redirect
from django.db import models
from decimal import Decimal
from django.db.models import Q

from .blockchain import Blockchain

blockchain = Blockchain()


def get_balance(user):
    sent_amount = Transaction.objects.filter(sender=user).aggregate(
        total=models.Sum("amount")
    )["total"] or Decimal("0.00")

    received_amount = Transaction.objects.filter(recipient=user).aggregate(
        total=models.Sum("amount")
    )["total"] or Decimal("0.00")

    return received_amount - sent_amount


def has_sufficient_balance(amount, user):
    current_balance = get_balance(user)
    return current_balance >= amount


def make_transaction(sender, receiver, amount, private_key):
    sender_user = CustomUser.objects.get(username=sender)
    receiver = receiver.strip().replace("\r\n", "\n")

    try:
        receiver_user = CustomUser.objects.get(
            Q(username=receiver) | Q(public_key=receiver)
        )
    except:
        return "Invalid Receiver"

    amount = float(amount)
    msg = f"{sender_user.username}->{receiver_user.username}:{amount:.2f}"

    if sender_user == receiver_user:
        return "Cannot Send to Yourself"

    if receiver_user.username in ["system", "admin"]:
        return "Cannot Send to System or Admin"

    try:
        signature = sign_data(msg.encode(), private_key)
    except ValueError:
        return "INVALID PRIVATE KEY FILE"

    if not has_sufficient_balance(amount, sender_user):
        return "Insufficient Balance"

    if not verify_signature(msg.encode(), signature, sender_user.public_key):
        return "Invalid Signature"

    transaction = Transaction.objects.create(
        sender=sender_user, recipient=receiver_user, amount=amount, signature=signature
    )

    # Blockchain logic

    blockchain.add_transaction(transaction)

    # blockchain.unconfirmed_transactions:
    return "Transaction Successful"
