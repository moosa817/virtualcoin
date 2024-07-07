import time
import hashlib
import json
from .models import Block, Transaction


class Blockchain:
    difficulty = 2
    block_size = 2  # Max number of transactions per block

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = self.load_chain()

    def load_chain(self):
        return list(Block.objects.all().order_by("index"))

    def get_last_block(self):
        return self.chain[-1] if self.chain else None

    def add_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)
        if len(self.unconfirmed_transactions) >= Blockchain.block_size:
            self.mine()

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.get_last_block()
        last_hash = last_block.hash if last_block else "0"
        new_block = Block(
            index=last_block.index + 1 if last_block else 0,
            previous_block=last_block,
            nonce=0,
        )

        # Save the block first to get its ID
        new_block.save()

        # Add up to block_size transactions to the new block
        transactions_to_include = self.unconfirmed_transactions[: Blockchain.block_size]
        new_block.transactions.set(transactions_to_include)

        while not self.is_valid_nonce(new_block):
            new_block.nonce += 1

        new_block.hash = new_block.compute_hash()
        new_block.save()  # Save again after hash and nonce are computed

        self.chain.append(new_block)
        self.unconfirmed_transactions = self.unconfirmed_transactions[
            Blockchain.block_size :
        ]
        return new_block

    def is_valid_nonce(self, block):
        guess_hash = self.compute_hash(block)
        return guess_hash.startswith("0" * Blockchain.difficulty)

    def compute_hash(self, block):
        return block.compute_hash()
