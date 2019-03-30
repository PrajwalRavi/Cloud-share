import random


class Transaction:
    def __init__(self, table_name, description, data_cost, owner):
        self.transaction_id = Transaction.generate_random_id()
        self.owner = owner
        self.table_name = table_name
        self.description = description
        self.data_cost = data_cost

    @staticmethod
    def generate_random_id():
        return str(hex(random.randrange(20000, 50000, 3)))[2:]
