import datetime
import hashlib

import boto3


class User:
    def __init__(self, uid):
        self.user_id = uid

    def view_user(self):
        print("\nUser " + str(self.user_id) + "'s Transactions:\n")
        for block in blockchain.chain:
            for trans in block.transactions:
                if trans.owner_id == self.user_id:
                    print("Table name: " + trans.table_name)
                    print("Description: " + trans.description)
                    print("Cost: $" + str(trans.data_cost))
                    print("\n")


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
            self.owners[transaction] = transaction.owner_id


class Transaction:
    def __init__(self, table_name, description, data_cost, owner_id):
        self.owner_id = owner_id
        self.table_name = table_name
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

        for trans in self.pending_transactions:
            new_block.transactions.append(trans)

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

    def add_data(self, table_name, description, cost, user):
        trans_obj = Transaction(table_name, description, cost, user.user_id)
        self.pending_transactions.append(trans_obj)

    def print_details(self):
        for block in self.chain:
            print(block)
            num = 1
            for trans in block.transactions:
                print("\n")
                print(trans.table_name + " : " + trans.description)
                table = dynamodb.Table(trans.table_name)
                print(table.scan())
                num += 1


dynamodb = boto3.resource('dynamodb')

blockchain = Blockchain()

table1_name = "Forum"
table2_name = "ProductCatalog"

user1 = User(1)
user2 = User(2)

print("Mining block 1 ........")
blockchain.add_data(table1_name, "This table describes the features of some forums", 60, user1)

print("Mining block 2 ........")
blockchain.add_data(table2_name, "This table has sample data by Amazon", 56, user1)

blockchain.mine_pending_transactions(5)
# blockchain.print_details()
user1.view_user()
