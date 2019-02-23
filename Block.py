import datetime
import hashlib


class User:
    def __init__(self, uid, uname, uage):
        self.u_id = uid
        self.u_name = uname
        self.u_age = uage


class Block:
    def __init__(self, timestamp, pending_transactions, prev_hash=""):
        self.timestamp = timestamp
        self.pending_transactions = pending_transactions
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.miner_id = None
        self.owners = {}

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
            self.owners[transaction] = transaction.owner_id


class Transaction:
    def __init__(self, table_ptr, description, data_cost, owner_id):
        self.owner_id = owner_id
        self.table_ptr = table_ptr
        self.description = description
        self.data_cost = data_cost


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []

    @staticmethod
    def create_genesis_block():
        return Block(datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, reward_address):  # reward address is the user id of the miner
        latest_block = self.get_latest_block()
        new_block = Block(datetime.datetime.now(), self.pending_transactions, latest_block.hash)
        new_block.mine_block(self.difficulty, reward_address)

        self.pending_transactions = []

        ############################
        # Zero knowledge proof
        self.chain.append(new_block)
        ############################

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            curr_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if curr_block.calculate_hash() != curr_block.hash or curr_block.prev_hash != prev_block.hash:
                # 1st cond : Checks current block's integrity
                # 2nd cond : If a user changes data of a block and calls calculate_hash(), the previous condn cannot
                return False

        return True
        # catch it , but this condition catches it

    def add_data(self, description, table_ptr, cost, user_id):
        trans_obj = Transaction(table_ptr, description, cost, user_id)
        self.pending_transactions.append(trans_obj)


blockchain = Blockchain()
print("Mining block 1 ........")
blockchain.add_data("Prajwal", "vsfgd", 60, 5)
print("Mining block 2 ........")
blockchain.add_data("Athilesh", "vsgfdg", 56, 6)
blockchain.mine_pending_transactions(5)
print(blockchain.chain)
