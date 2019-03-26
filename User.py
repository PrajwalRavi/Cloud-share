import hashlib

from Transaction import Transaction

class User:
    def __init__(self):
        self.user_id = Transaction.generate_random_id()
        self.wallet_address = hashlib.sha256(self.user_id.encode())

    def view_user(self, blockchain):
        print("\nUser " + str(self.user_id) + "'s Transactions:\n")
        for block in blockchain.chain:
            for trans in block.transactions:
                if trans.owner.user_id == self.user_id:
                    print("Table name: " + trans.table_name)
                    print("Description: " + trans.description)
                    print("Cost: $" + str(trans.data_cost))
                    print("\n")
