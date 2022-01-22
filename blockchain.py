from hashlib import sha256

hash_func = lambda x: sha256(str(x).encode('utf-8')).hexdigest()


class Block:
    def __init__(self, data, prev):
        self.data = data
        self.prev = prev
        if prev is not None:
            self.hashed_prev_data = hash_func(prev.data)


class Blockchain:

    def __init__(self):
        self.head = Block('genesis', None)

    def add_block(self, data):
        self.head = Block(data, self.head)

def get_chain(chain):
    chain_data = []
    curr = chain.head
    print(curr.data)
    chain_data.append(curr.data)
    while curr.prev is not None:
        if curr.hashed_prev_data == hash_func(curr.prev.data):
            chain_data.append(curr.prev.data)
            print(curr.prev.data)
        curr = curr.prev
    return chain_data