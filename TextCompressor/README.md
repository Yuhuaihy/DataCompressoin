This is a text compressor and decompressor using dynamic dictionary.
The dictionary size is 64K, the pointer is 16-bit.
To implement the code, modify TestDriver.py.
Compressor(filepath, method='FC', deletion= 'RESTART')
filepath is the test file path.
method is updating method, could be 'FC' or 'CM',
deletion could be 'FREEZE' , 'RESTART' or 'LRU'.
Method export_compress_result() and export_decompress_result() could export compression and decompression result to a txt file. The compression result will be a string of binary. 
If the origin of text equals the decompression result, it will print out "The decompression result of {update method} update and {deletion method} deletion equals the origin text:  True".
