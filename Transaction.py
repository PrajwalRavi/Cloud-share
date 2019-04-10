import random


class Transaction:
    def __init__(self, table_name, description, data_cost, owner):
        self.transaction_id = Transaction.generate_random_id()
        self.owner = owner
        self.table_name = table_name
        self.description = description
        self.data_cost = data_cost

    def verify_transaction(self):
        A = self.owner.publicA
        p = self.owner.publicP
        B = (A ** self.data_cost) % p
        print("A= " + str(A) + " p= " + str(p))

        rounds = 3
        for num in range(0, rounds):
            print("\nVerification - Round " + str(num + 1))
            print("\nChoose random r from 0 to p-1")
            print("Calculate A^r(mod p) and enter the value: ")  # 9
            h = int(input())
            b = random.randint(0, 1)
            print("\nAssume the bit b = " + str(b))
            print("Calculate (r+bx)(mod(p-1)) taking x = cost of product, and enter the value: ")  # 6 if b=0
            s = int(input())
            if ((A ** s) % p) != ((h * (B ** b)) % p):
                return False

        print("Identity successfully verified.")
        return True

    def __str__(self):
        transaction_detail = "Transaction ID: " + str(self.transaction_id) + "\nTable name: " + str(
            self.table_name) + "\nDescription" + self.description + "\n"
        return transaction_detail

    @staticmethod
    def generate_random_id():
        return str(hex(random.randrange(20000, 50000, 3)))[2:]
