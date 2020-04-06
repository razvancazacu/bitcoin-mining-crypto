import hashlib
import struct
import multiprocessing
from time import time
import random
from numba import jit, cuda

def get_target_str(bits):
    exp = bits >> 24
    mant = bits & 0xffffff
    target_hexstr = '%064x' % (mant * (1 << (8 * (exp - 3))))
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
                  nonce_max_val):
    n_processes = 8
    batch_size = int(5.0e5)
    pool = multiprocessing.Pool(n_processes)
    start_nonce_val = nonce
    while True:
        nonce_ranges = [
            (nonce + i * batch_size, nonce + (i + 1) * batch_size)
            for i in range(n_processes)
        ]

        params = [
            (version,
             prev_block,
             merkle_root,
             timestamp,
             bits_diff,
             nonce_range[0], nonce_range[1]) for nonce_range in nonce_ranges
        ]

        # Single-process search:
        # solutions = map(find_solution, params)

        # Multi-process search:

        if nonce < nonce_max_val:
            solutions_exercise_1 = start_process_pool(nonce_ranges, params, pool)
            if len(solutions_exercise_1):
                print("Reached selected iteration end")
                print("Start nonce is:", start_nonce_val)
                print("End nonce is:", nonce)
                return solutions_exercise_1
            nonce += n_processes * batch_size
        else:
            print("Reached selected iteration end")
            print("Start nonce is:", start_nonce_val)
            print("End nonce is:", nonce)

            break


def start_process_pool(nonce_ranges, params, pool):
    solutions_pool = pool.map(find_nonce_multiproc, params)
    print('Searched %d to %d' % (nonce_ranges[0][0], nonce_ranges[-1][1] - 1))
    solutions_pool = list(filter(lambda x: (x is not None), solutions_pool))
    return solutions_pool


if __name__ == '__main__':
    start = time()
    version = 0x20400000
    prev_block = "00000000000000000006a4a234288a44e715275f1775b77b2fddb6c02eb6b72f"
    merkle_root = "2dc60c563da5368e0668b81bc4d8dd369639a1134f68e425a9a74e428801e5b8"
    timestamp = 0x5DB8AB5E
    bits_diff = 0x17148EDF
    start_nonce = 0xB2D05E00
    end_nonce = 0xB8C63F00
    start_nonce = 3000000000

    # -------  1  -------
    solutions = proof_of_work(version, prev_block, merkle_root, timestamp, bits_diff, start_nonce, end_nonce)

    # solutions = proof_of_work(version, prev_block, merkle_root, timestamp, bits_diff, 3168331852, 4294967296)

    # # print('\n'.join('%d => %s' % s for s in solutions)) # for multiple solutions found
    print('Solution (ex 1) found in %.3f seconds' % (time() - start))
    # ------ VERIF Given Ex ------
    print("Is the given hash equal to the resulting one?:", verify_nonce(0x3fff0000,
                                                                         "0000000000000000000140ac4688aea45aacbe7caf6aaca46f16acd93e1064c3",
                                                                         "422458fced12693312058f6ee4ada19f6df8b29d8cac425c12f4722e0dc4aafd",
                                                                         0x5E664C76,
                                                                         0x17110119,
                                                                         538463288) == "0000000000000000000d493c3c1b91c8059c6b0838e7e68fbcf8f8382606b82c")

    # ------ VERIF EX 1 ------
    print("Is hashing still valid?:", verify_nonce(version,
                                                   prev_block,
                                                   merkle_root,
                                                   timestamp,
                                                   bits_diff,
                                                   3060331852) == "0000000000000000000d7612d743325d8e47cb9e506d547694478f35f736188e")

    # -------  2  -------
    # 2 ^ 32 = 4294967296
    maximum_nonce_value = 4294967296 - 100000000
    start_nonce = random.randrange(3060331853, maximum_nonce_value)
    end_nonce = start_nonce + 100000000
    solutions = proof_of_work(version, prev_block, merkle_root, timestamp, bits_diff, start_nonce,
                              end_nonce)

    print('Solution (ex 2) found in %.3f seconds' % (time() - start))
