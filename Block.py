import datetime
import hashlib


class Block:
    def __init__(self, index, timestamp, data, prev_hash=""):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return str(hashlib.sha256(
            (self.data + str(self.index) + self.prev_hash + str(self.timestamp)).encode()).hexdigest())


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    @staticmethod
    def create_genesis_block():
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_data(self, data):
        old_block = self.get_latest_block()
        new_block = Block(old_block.index + 1, datetime.datetime.now(), data, old_block.hash)
        # Zero knowledge proof
        self.chain.append(new_block)

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            curr_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if curr_block.calculate_hash() != curr_block.hash or curr_block.prev_hash != prev_block.hash:
                # 1st condn : Checks current block's integrity
                # 2nd condn : If a user changes data of a block and calls calculate_hash(), the previous condn cannot
                # catch it , but this condition catches it
                return False
        return True


blockchain = Blockchain()
blockchain.add_data("Prajwal")
blockchain.add_data("Athilesh")

# for block in blockchain.chain:
#     print(block.__dict__)

# print(blockchain.verify_chain())
blockchain.chain[-2].index = 64
blockchain.chain[-2].hash = blockchain.chain[-2].calculate_hash()
print(blockchain.verify_chain())
