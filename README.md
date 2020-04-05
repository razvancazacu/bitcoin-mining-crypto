# Bitcoin Mining Project
### [Bitcoin Mining:](http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html)
Uses hash function *double SHA-256*. The short way of explaining it is: "*A hash takes a chunk of data as input and shrinks it down into a smaller hash value (in this case 256 bits)*"

To mine a block, you first :

- collect the new transactions into a block. 
- hash the block to form a 256-bit block hash value.
- If the hash starts with enough zeros, the block has been successfully mined and is sent into the Bitcoin network and the hash becomes the identifier for the block.

 Most of the time the hash isn't successful, so you modify the block slightly and try again, over and over billions of times. About every 10 minutes someone will successfully mine a block, and the process starts over.
 
---
 
 ### Bitcoin Block Structure

 - Protocol version 
 - Previous block hash 
 - Merkle root (hash of all transactions from the block)
 - Timestamp of the block
 - Bits (mining difficulty)
 - **Nonce** (Value incremented on each hash to provide a new hash value)

 Each nonce value generates a b-random hash value. That means it is needed to try an exponentially large number of nonces to find a hash with enough zeroes
 
 
 ## Problem
#### 1. Find the Hash value with the numbers of 0 according to the given difficulty and the Nonce value between 3 000 000 000 and 3 100 000 000

|  Field | Value  |  
|---|---|
| Version  | 0x20400000  |  
| Prev Block  | 00000000000000000006a4a234288a44e715275f1775b77b2fddb6c02eb6b72f  |   
|  Merkle Root |  2dc60c563da5368e0668b81bc4d8dd369639a1134f68e425a9a74e428801e5b8 |   
|Timestamp|0x5DB8AB5E|
|Bits|0x17148EDF|

#####_Results Solution found in 92.675 seconds_
- Nonce value: 3060331852
- Hash value: 0000000000000000000d7612d743325d8e47cb9e506d547694478f35f736188e

**_First 5 Hash values_**

|Nonce|Hash|
|---|---|
|3000000000 | 70ba305ff525556330ab7f3fc3f342f2e82acd8d896e52dee84c0fec07fd8881|
|3000000001 | e16392883f05773debd5be4f8e9b99d3445c3539b031cd857ac0dc48de85c3f4|
|3000000002 | e7becb7c0bc3b14370dc33f289822e61b706febaae6f0ba7b9c96f4c0e31ffed|
|3000000003 | 741fe37c2260738ceaeab90429b8adce1f1c1887a2a43855a79353cf35725e05|
|3000000004 | be3336f846a487f00de37b1c7565e6dcf600b25fbb54025cc7776337b5d6ebc1|

#### **Methods used:**

- Single process iterating over the nonce values
- Multiprocess (8) iterating over the nonce values with 250000 values per process (93.384s)
- Multiprocess (8) iterating over the nonce values with 1000000 values per process (92.675s)

_A possible faster method is using the CUDA cores from the GPU_