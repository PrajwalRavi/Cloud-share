import datetime
import hashlib


class User:

    def __init__(self, uid, uname, uage):
        self.Uid = uid
        self.Uname = uname
        self.Uage = uage



class Block:
    def __init__(self, timestamp, data, prev_hash=""):
        # self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.minerid  = None

    def calculate_hash(self):
        return str(hashlib.sha256(
            (self.data + self.prev_hash + str(self.timestamp) + str(
                self.nonce)).encode()).hexdigest())

    def mine_block(self, difficulty,uid):
        while self.hash[0:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        self.minerid = uid


class Transaction:
    def __init__(self,table_ptr,description,data_cost,rewardee_list):
        pass


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 5
        self.pending_transactions = []
        self.mining_reward = 100

    @staticmethod
    def create_genesis_block():
        return Block(datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, rewardaddress, data): #reward address is the user id of the miner
        old_block = self.get_latest_block()
        new_block = Block(datetime.datetime.now(), self.pending_transactions, old_block.hash)
        new_block.mine_block(self.difficulty,rewardaddress)

        self.pending_transactions = []
        # print(new_block.hash)
        # Zero knowledge proof
        self.chain.append(new_block)
        #
        # def add_data(self, data):
        #     old_block = self.get_latest_block()
        new_block = Block(datetime.datetime.now(), data, old_block.hash)

    #     new_block.mine_block(self.difficulty)
    #     print(new_block.hash)
    #     # Zero knowledge proof
    #     self.chain.append(new_block)

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            curr_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if curr_block.calculate_hash() != curr_block.hash or curr_block.prev_hash != prev_block.hash:
                # 1st condn : Checks current block's integrity
                # 2nd condn : If a user changes data of a block and calls calculate_hash(), the previous condn cannot
                return False

        return True
        # catch it , but this condition catches it

    def add_data(self, data):
        trans_obj = Transaction(data)
        self.pending_transactions.append(trans_obj)
        pass


blockchain = Blockchain()
print("Mining block 1 ........")
blockchain.add_data("Prajwal")
print("Mining block 2 ........")
blockchain.add_data("Athilesh")
