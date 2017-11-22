from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_connection = None

def start():
    address = "140.112.29.42"
    port = "8332"
    #please fill this on your own :)
    password = None
    username = "2b"
    global rpc_connection
    rpc_connection = AuthServiceProxy("http://{}:{}@{}:{}".format(username, password, address, port))

def flatten(l):
    ans = []
    for i in l:
        ans += i
    return ans

def call_method(*args):
    return rpc_connection.batch_([list(args)])[0]

def get_block_hash(height):
    return call_method("getblockhash", height)

def get_block(block_hash):
    return call_method("getblock", block_hash)

def get_transactions(tids):
    commands = [["getrawtransaction", tid, 1] for tid in tids]
    return rpc_connection.batch_(commands)

def get_block_count():
    return call_method("getblockcount")

def get_output_addresses(transaction):
    ans = set()
    for l in transaction["vout"]:
        ans |= set(l.get("scriptPubKey", {}).get("addresses", []))
    return ans

def get_input_addresses(transaction):
    ans = []
    txs_in = []
    numbers_in = []
    for l in transaction["vin"]:
        if "txid" in l:
            txs_in.append(l["txid"])
            numbers_in.append(l["vout"])
    for tx, num in zip(get_transactions(txs_in), numbers_in):
        addresses = tx["vout"][num].get("scriptPubKey", {}).get("addresses", [])
        ans += addresses
    return set(ans)

#returning a pair (received_from, sent_to) of all the addresses from witch the `analised_address`
#received the money and all the addresses to whitch the `analised_address` sent the money.
def analize_transaction(analized_address, transaction):
    output_addresses = get_output_addresses(transaction)
    input_addresses = get_input_addresses(transaction)
    in_ans = set() if analized_address not in output_addresses else input_addresses
    out_ans = set() if analized_address not in input_addresses else output_addresses
    return (out_ans, in_ans)

#merging the results of analize transaction function
def merge(t1, t2):
    received1, sent1 = t1
    received2, sent2 = t2
    return (received1 | received2, sent1 | sent2)

def analize_block(analized_address, block):
    ans = (set(), set())
    transactions = get_transactions(block.get("tx", []))
    i = 0
    c = len(transactions)
    for transaction in transactions:
        print("transaction {} out of {}".format(i,c))
        i += 1
        data = analize_transaction(analized_address, transaction)
        ans = merge(ans, data)
    return ans

def analize_block_by_height(analized_address, block_height):
    block_hash = get_block_hash(block_height)
    block = get_block(block_hash)
    return analize_block(analized_address, block)

def analize_blocks_from_range(analized_address, start, end):
    ans = (set(), set())
    for i in range(start, end+1):
        print(i)
        data = analize_block_by_height(analized_address, i)
        ans = merge(ans, data)
    return ans

def analize_chain(analized_address, blocks_no):
    last = get_block_count()
    # 0-th block has only one coinbase transaction, that for some reason "never really happend"
    # https://github.com/bitcoin/bitcoin/issues/3303
    first = max(1, last - blocks_no)
    return analize_blocks_from_range(analized_address, first, last-1)

start()
x = analize_chain("1NmTeRGtEhD7rjhzHVEdWwAxxpmHrbbEpo", 3)
print(x)


# rpc_user and rpc_password are set in the bitcoin.conf file
#print("ok")
#best_block_hash = rpc_connection.getbestblockhash()
#print(rpc_connection.getblock(best_block_hash))
#bitcoin_address = "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy"
#command = [["getblockhash", 0]]
#block_hash = rpc_connection.batch_(command)[0]
#command = [["getblock", block_hash]]
#block_info = rpc_connection.batch_(command)[0]["tx"]
#commands = [["getrawtransaction", transaction_hash, 1] for transaction_hash in block_info]
#print(commands)
#transactions = rpc_connection.batch_(commands)
#for transaction in transactions:
#    receivers = transaction["vout"]
#    print receivers


#print block_info
#commands = [ [ "getblockhash", height] for height in range(100) ]
#block_hashes = rpc_connection.batch_(commands)
#blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
#block_times = [ block["time"] for block in blocks ]
#print(block_times)
