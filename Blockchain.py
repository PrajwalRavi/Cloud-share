import datetime

import boto3

from Block import Block
from Transaction import Transaction
from User import User


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
        trans_obj = Transaction(table_name, description, cost, user)
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

    def purchase(self, user):
        print("\nID \t\t   Cost \t\t Description")
        data_cost = {}
        for block in self.chain:
            for transaction in block.transactions:
                data_cost[transaction.transaction_id] = transaction.data_cost
                print(transaction.transaction_id, end="\t\t")
                print("$" + str(transaction.data_cost), end="\t\t")
                print(transaction.description)
        print("\nEnter ID of the data you would like to buy: ")
        option = input().strip()
        while option not in data_cost.keys():
            option = input().strip()

#     TO-DO : CLEAN UP OLD CODE TO USE User OBJECT INSTEAD OF ID. THEN WRITE CODE TO PERFORM TRANSACTIONS.


if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb')

    blockchain = Blockchain()

    table1_name = "Forum"
    table2_name = "ProductCatalog"

    user1 = User()
    user2 = User()

    print("Mining block 1 ........")
    blockchain.add_data(table1_name, "This table describes the features of some forums.", 60, user1)

    print("Mining block 2 ........")
    blockchain.add_data(table2_name, "This table has sample data by Amazon.", 56, user1)

    blockchain.mine_pending_transactions(5)
    # blockchain.print_details()
    # user1.view_user(blockchain)
    blockchain.purchase(user2)