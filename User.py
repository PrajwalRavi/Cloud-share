import hashlib

from Transaction import Transaction


class User:
    def __init__(self):
        self.user_id = Transaction.generate_random_id()
        self.wallet_address = hashlib.sha256(self.user_id.encode())
        self.purchases = []

    def view_user(self, blockchain):
        print("\nUser " + str(self.user_id) + "'s Transactions:\n")
        for block in blockchain.chain:
            for trans in block.transactions:
                if trans.owner.user_id == self.user_id:
                    print("Table name: " + trans.table_name)
                    print("Description: " + trans.description)
                    print("Cost: $" + str(trans.data_cost))
                    print("\n")

        print("\nUser " + str(self.user_id) + "'s Purchases:")
        if len(self.purchases) == 0:
            print("No purchases till date")
        else:
            num = 1
            for transaction in self.purchases:
                print(str(num) + ") " + str(transaction.transaction_id) + " " + str(transaction.table_name) + " " + str(
                    transaction.description))
                num += 1
