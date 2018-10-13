General Description:
Implement an adaptive text compressor.

Options
Option 1: Dynamic Dictionary Compressor
Write a dynamic dictionary compressor (and a corresponding decompressor) that has at least two encoding options, FC and one you choose (e.g., AP), and three deletion options, FREEZE (simply stop adding entries when the dictionary fills) RESTART (reset the dictionary whenever it is full and compression drops off according to some criterion you choose), and LRU. For simplicity, you may use a dictionary of size 64K where pointers always use 16 bits, even while the dictionary is growing. Or for extra credit, you can have variable size pointer that grow until the dictionary is filled, and the dictionary size can be a parameter You should employ an efficient data structure to store and access the dictionary.
Option 2: Sliding Window Compressor
Write a sliding window compressor (and a corresponding decompressor). For simplicity, you may use a fixed size 16-bit encoding of pointers (see the lecture slides). Or for extra credit, use a variable length coding of pointers of your choice. Your encoder should employ hashing data structure for searching for matches. The window size should be a parameter.