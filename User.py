import hashlib

from Transaction import Transaction


class User:
    def __init__(self):
        self.user_id = Transaction.generate_random_id()
        self.wallet_address = hashlib.sha256(self.user_id.encode())
        self.purchases = []
        self.publicA = 2
        self.publicP = 11

    def view_user(self, blockchain):
        print("***************************************************************************")
        print("User ID:" + str(self.user_id))
        print("Transactions:")
        for block in blockchain.chain:
            for trans in block.transactions:
                if trans.owner.user_id == self.user_id:
                    print("****************************************")
                    print("Table name: " + trans.table_name)
                    print("Description: " + trans.description)
                    print("Cost: $" + str(trans.data_cost))
                    print("\n")

        print("User " + str(self.user_id) + "'s Purchases:")
        if len(self.purchases) == 0:
            print("No purchases till date")
        else:
            num = 1
            for transaction in self.purchases:
                print("****************************************")
                print(str(num) + ") " + str(transaction))
                num += 1
        print("*****************************************************************************************************************")
