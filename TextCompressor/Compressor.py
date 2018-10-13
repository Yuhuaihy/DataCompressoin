import os
from IPython import embed
import time
DICT_SIZE = 65536

def deletion_freeze():
    pass

def deletion_restart(dict):
    pass
def deletion_LRU(dict):
    pass

def update_dict(dictionary, key, deletion):
    if key in dictionary:
        return
    if len(dictionary) < DICT_SIZE:
        dictionary[key] = len(dictionary)
        return 
    if deletion == 'FREEZE':
        deletion_freeze()
    elif deletion == 'RESTART':
        deletion_restart()
    elif deletion == 'LRU':
        deletion_LRU()



def FC_compressor(data, dictionary, deletion):
    prev = ''
    n = len(data)
    compress_result = []
    head = 0
    tail = 1
    while tail <= n:
        cur_len = len(dictionary)
        while data[head:tail] in dictionary and tail <= n:
            tail += 1
        current_match = data[head:tail-1]
        compress_result.append(dictionary[current_match])
        update = prev + current_match[0]
        update_dict(dictionary, update, deletion)
        
        prev = current_match
        head = tail -1
        tail = head + 1
    return compress_result



def NC_compressor(data, dictionary, deletion):
    n = len(data)
    compress_result = []
    head = 0
    tail = 1
    while tail <= n:
        cur_len = len(dictionary)
        while data[head:tail] in dictionary and tail <= n:
            tail += 1
        current_match = data[head:tail-1]
        compress_result.append(dictionary[current_match])
        update = current_match + data[tail-1] if tail -1 < n else current_match
        update_dict(dictionary, update, deletion)
        head = tail -1
        tail = head + 1
    return compress_result

    


class Compressor:

    def __init__(self,filepath, method = 'FC', deletion = 'FREEZE', data = None, outpath = 'results'):
        try:
            with open(filepath,'r') as f:
                self.datasetname = filepath.rsplit('/',1)[-1]
                self.data = f.read()
        except IOError:
            print("File is not accessible.")
        if data:
            self.data = data
        characters = set(self.data)
        self.dictionary = dict(zip(characters, range(len(characters))))
        self.method = method
        self.deletion = deletion
        self.outpath = outpath
    
    def compress(self):
        if self.method == 'FC':
            self.compress_result = FC_compressor(self.data, self.dictionary, self.deletion)
        elif self.method == 'NC':
            self.compress_result = NC_compressor(self.data, self.dictionary, self.deletion)
        else:
            print('Sorry %d is not supported'%self.method)

    def decompress(self):
        pass

    def export_compress_result(self):
        filename = self.datasetname + '-' + str(round(time.time())) + '.txt'
        path = os.path.join(self.outpath,filename)
        with open(path, 'w') as f:
            f.write(str(self.compress_result))
            






    
        

        
