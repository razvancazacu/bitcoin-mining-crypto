# Bitcoin Mining Project
### [Bitcoin Mining:](http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html)
Uses hash function *double SHA-256*.

[]: *A hash takes a chunk of data as input and shrinks it down into a smaller hash value (in this case 256 bits)*

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