from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import hashlib
import json
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(null=True, blank=True)
    public_key = models.TextField()
    is_new_user_setup_completed = models.BooleanField(default=False)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        CustomUser, related_name="sent_transactions", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        CustomUser, related_name="received_transactions", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    signature = models.TextField()  # Store signature of the transaction

    def __str__(self):
        return f"{self.sender.username}->{self.recipient.username}:{self.amount}"


from django.db import models
from django.utils import timezone
import hashlib
import json


class Block(models.Model):
    index = models.IntegerField(unique=True)
    previous_block = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="next_blocks",
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(default=timezone.now)
    nonce = models.IntegerField()
    hash = models.CharField(max_length=64, unique=True)
    transactions = models.ManyToManyField("Transaction")

    def save(self, *args, **kwargs):
        # Save the block without transactions first to get an ID
        if not self.pk:  # If the block hasn't been saved to the database yet
            super().save(*args, **kwargs)

        # Compute the hash and save the block again with transactions
        self.hash = self.compute_hash()
        super().save(*args, **kwargs)

    def compute_hash(self):
        block_dict = self.to_dict()
        block_string = json.dumps(block_dict, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_block.hash if self.previous_block else None,
            "timestamp": str(self.timestamp),
            "nonce": self.nonce,
            "transactions": [str(tx.id) for tx in self.transactions.all()],
        }

    def __str__(self):
        return f"Block {self.index} with hash {self.hash}"
