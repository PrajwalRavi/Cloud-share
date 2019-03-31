import hashlib
import random


class Block:
    # Each block can consist of multiple transactions
    def __init__(self, timestamp, pending_transactions, prev_hash=""):
        self.timestamp = timestamp
        self.pending_transactions = pending_transactions
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.miner = None
        self.transactions = []
        self.beneficiaries = {}

    def __str__(self):
        assert self.miner is not None
        return str(self.timestamp) + "  " + str(self.miner.user_id)

    def calculate_hash(self):
        str_transactions = ""
        for trans in self.pending_transactions:
            str_transactions += str(trans)

        return str(hashlib.sha256(
            (str_transactions + self.prev_hash + str(self.timestamp) + str(self.nonce)).encode()).hexdigest())

    def mine_block(self, difficulty, miner):
        while self.hash[0:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

        # Owner and the miner to be paid on purchase_data of the transaction
        self.miner = miner
        for transaction in self.pending_transactions:
            self.beneficiaries[transaction.transaction_id] = transaction.owner.user_id

    def verify_block(self):
        check = 0
        for transaction in self.transactions:
            A = self.miner.publicA
            p = self.miner.publicP
            B = (A ** transaction.data_cost) % p

            for num in range(0, 1):
                print("\nVerification - Round " + str(num + 1))
                print("\nChoose random r from 0 to p-1")
                print("Calculate A^r(mod p) and enter the value: ")  # 9
                h = int(input())
                b = random.randint(0, 1)
                b = 0
                print("\nAssume the bit b = " + str(b))
                print("Calculate (r+bx)(mod(p-1)) taking x = cost of product, and enter the value: ")  # 6 if b=0
                s = int(input())
                if ((A ** s) % p) == ((h * (B ** b)) % p):
                    check = check + 1

        if check == 1 * len(self.transactions):
            print("Identity successfully verified.")
            return True
        else:
            return False
