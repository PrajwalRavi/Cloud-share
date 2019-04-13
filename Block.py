import hashlib


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
        block_details = "Block creation time: " + str(self.timestamp) + "\nMined by: " + str(self.miner.user_id)
        return block_details

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
            transaction.benefeciaries.append(miner)
