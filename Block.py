import hashlib


class Block:
    def __init__(self, timestamp, pending_transactions, prev_hash=""):
        self.timestamp = timestamp
        self.pending_transactions = pending_transactions
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.miner_id = None
        self.transactions = []
        self.owners = {}

    def __str__(self):
        return str(self.timestamp) + "  " + str(self.miner_id)

    def calculate_hash(self):
        str_transactions = ""
        for trans in self.pending_transactions:
            str_transactions += str(trans)

        return str(hashlib.sha256(
            (str_transactions + self.prev_hash + str(self.timestamp) + str(self.nonce)).encode()).hexdigest())

    def mine_block(self, difficulty, uid):
        while self.hash[0:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

        # Owner and the miner to be paid on purchase of the transaction
        self.miner_id = uid
        for transaction in self.pending_transactions:
            self.owners[transaction] = transaction.owner.user_id
