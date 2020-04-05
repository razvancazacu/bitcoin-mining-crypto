
import hashlib, struct, binascii
def f(x):
    return x*x

def get_target_str_worker(bits):
    # https://en.bitcoin.it/wiki/Difficulty
    exp = bits >> 24
    mant = bits & 0xffffff
    target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
    print("T:",target_hexstr)
    
    target_str = bytes.fromhex(target_hexstr)
    return target_str
    #   print(target_str)

def find_nonce_multiproc(args):
    print("Checkpoint - start nonce")
    print(len(args))
    print(args)
    version, prev_block, mrkl_root, timestamp, bits_difficulty, starting_nonce, end_nonce = args
    target_str = get_target_str_worker(bits_difficulty)
    #   L - unsinged Long
    #   < - little endian
    if starting_nonce > end_nonce:
        print("WRONG NONCE INPUT!")
    else:
        nonce = starting_nonce
        while starting_nonce < end_nonce:
            header = ( struct.pack("<L", version) + 
                      bytes.fromhex(prev_block)[::-1] +
                      bytes.fromhex(mrkl_root)[::-1] +
                      struct.pack("<LLL", timestamp, bits_difficulty, nonce))
            hash_result = hashlib.sha256(hashlib.sha256(header).digest()).digest()

            if nonce % 1000000 == 0 or nonce in range(3000000000,3000000005):
                print(nonce)
                print(bytes.hex(hash_result[::-1]))

            if hash_result[::-1] < target_str:
                print("Nonce value:\n", nonce)
                print("Hash value:\n",bytes.hex(hash_result[::-1]))
                print('success')
                return nonce
                break
            
            nonce += 1
    return None