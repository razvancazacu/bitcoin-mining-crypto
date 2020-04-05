import hashlib
import struct
import binascii
import multiprocessing
from time import time

def get_target_str(bits):

    exp = bits >> 24
    mant = bits & 0xffffff
    target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
    target_str = bytes.fromhex(target_hexstr)

    return target_str


def verify_nonce(version, prev_block, mrkl_root,
                 timestamp, bits_difficulty, nonce):
    target_str = get_target_str(bits_difficulty)
    header = (struct.pack("<L", version) +
              bytes.fromhex(prev_block)[::-1] +
              bytes.fromhex(mrkl_root)[::-1] +
              struct.pack("<LLL", timestamp, bits_difficulty, nonce))
    hash_result = hashlib.sha256(hashlib.sha256(header).digest()).digest()

    return bytes.hex(hash_result[::-1])
    nonce += 1


def find_nonce_multiproc(args):
    version, prev_block, mrkl_root, timestamp, bits_difficulty, starting_nonce, end_nonce = args
    target_str = get_target_str(bits_difficulty)
    #   L - unsinged Long
    #   < - little endian

    while starting_nonce < end_nonce:
        header = (struct.pack("<L", version) +
                  bytes.fromhex(prev_block)[::-1] +
                  bytes.fromhex(mrkl_root)[::-1] +
                  struct.pack("<LLL", timestamp, bits_difficulty, starting_nonce))
        hash_result = hashlib.sha256(hashlib.sha256(header).digest()).digest()

        if starting_nonce % 1000000 == 0 or starting_nonce in range(3000000000, 3000000005):
            print("[Nonce level: ", starting_nonce, ", ", bytes.hex(hash_result[::-1]), "]")

        if hash_result[::-1] < target_str:
            print("Value found -> [ Nonce value:", starting_nonce, "Hash value:", bytes.hex(hash_result[::-1]), "]")
            return starting_nonce

        starting_nonce += 1
    return None


def proof_of_work(version,
                 prev_block,
                 merkle_root,
                 timestamp,
                 bits_diff,
                 nonce,
                 nonce_max):
    n_processes = 8
    batch_size = int(5.0e5)
    pool = multiprocessing.Pool(n_processes)

    while True:
        nonce_ranges = [
            (nonce + i * batch_size, nonce + (i+1) * batch_size)
            for i in range(n_processes)
        ]

        params = [
            (version,
             prev_block,
             merkle_root,
             timestamp,
             bits_diff,
             nonce_range[0],nonce_range[1]) for nonce_range in nonce_ranges
        ]

        # Single-process search:
        #solutions = map(find_solution, params)

        # Multi-process search:
        solutions = pool.map(find_nonce_multiproc, params)
        print('Searched %d to %d' % (nonce_ranges[0][0], nonce_ranges[-1][1]-1))
        solutions = list(filter(lambda x: (x is not None), solutions))
        if len(solutions):
            return solutions

        nonce += n_processes * batch_size

if __name__ == '__main__':
    start = time()
    version = 0x20400000
    prev_block = "00000000000000000006a4a234288a44e715275f1775b77b2fddb6c02eb6b72f"
    merkle_root = "2dc60c563da5368e0668b81bc4d8dd369639a1134f68e425a9a74e428801e5b8"
    timestamp = 0x5DB8AB5E
    bits_diff = 0x17148EDF
    start_nonce = 0xB2D05E00
    end_nonce = 0xB8C63F00
    start_nonce = 3060000000
    end_nonce = 3100000000

    # -------  1  -------
    solutions = proof_of_work(version, prev_block, merkle_root, timestamp, bits_diff, start_nonce, end_nonce)
    # print('\n'.join('%d => %s' % s for s in solutions)) # for multiple solutions found
    print('Solution (ex 1) found in %.3f seconds' % (time() - start))

    # -------  2  -------



    print('Solution (ex 2) found in %.3f seconds' % (time() - start))
