To implement the code,
modify TestDriver.py
Compressor(filepath, method='FC', deletion= 'RESTART')
filepath is the test file path.
method is updating method, could be 'FC' or 'CM',
deletion could be 'FREEZE' , 'RESTART' or 'LRU'.
method export_compress_result() could export compression result to a txt file. It will be a list of integers. (I will convert the compression result to binary strings later)
If the origin of text equals the decompression result, it will print out "The decompression result of FC update and RESTART deletion equals the origin text:  True"
