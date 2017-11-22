from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_connection = None

def start():
    address = "140.112.29.42"
    port = "8332"
    password = "please fill this"
    assert password != "please fill this"
    username = "2b"
    global rpc_connection
    if rpc_connection is None:
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

def split(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def get_transactions_simple(tids):
    commands = [["getrawtransaction", tid, 1] for tid in tids]
    command_small_lists = split(commands, 1000)
    answers = []
    for command_small_list in command_small_lists:
        print("calling {}".format(len(command_small_list)))
        answers += rpc_connection.batch_(command_small_list)
    return answers


cache = dict()
def get_transactions(tids):
    not_in_cache = [x for x in tids if x not in cache]
    if len(not_in_cache) > 0:
        print("calling with {}".format(len(not_in_cache)))
        ans = get_transactions_simple(not_in_cache)
        print("after")
    else:
        ans = []
    for transaction in ans:
        tid = transaction["txid"]
        cache[tid] = transaction
    return [cache[i] for i in tids]


def prepare_block(tids):
    cache.clear()
    transactions = get_transactions(tids)
    new_transactions = []
    for transaction in transactions:
        for l in transaction["vin"]:
            if "txid" in l:
                new_transactions.append(l["txid"])
    get_transactions(new_transactions)


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
    prepare_block(block.get("tx", []))
    transactions = get_transactions(block.get("tx", []))
    i = 0
    c = len(transactions)
    for transaction in transactions:
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
        print("block {}".format(i))
        data = analize_block_by_height(analized_address, i)
        ans = merge(ans, data)
    return ans

def analize_chain(analized_address, blocks_no):
    last = get_block_count()
    # 0-th block has only one coinbase transaction, that for some reason "never really happend"
    # https://github.com/bitcoin/bitcoin/issues/3303
    first = max(1, last - blocks_no)
    return analize_blocks_from_range(analized_address, first, last-1)
