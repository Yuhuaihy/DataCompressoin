import os
from IPython import embed
import time
DICT_SIZE = 65536

def deletion_freeze():
    pass

def deletion_restart(d, process):
    if process == 'compress':
        d = dict((chr(x), x) for x in range(128))
    else:
        d = dict((x,chr(x)) for x in range(128))
    return d
    
def deletion_LRU(d):
    pass

def update_dict(dictionary, key, deletion):
    if key in dictionary:
        return dictionary
    if len(dictionary) < DICT_SIZE:
        dictionary[key] = len(dictionary)
        return dictionary
    if deletion == 'FREEZE':
        return dictionary
    elif deletion == 'RESTART':
        print('=====Dictionary updated!======')
        dictionary = deletion_restart(dictionary, 'compress')
    elif deletion == 'LRU':
        deletion_LRU()
    
    return dictionary

def update_dict_decompress(dictionary, value, deletion):
    if value in dictionary.values():
        return dictionary
    n = len(dictionary)
    if len(dictionary) < DICT_SIZE:
        dictionary[n] = value
        return dictionary
    if deletion == 'FREEZE':
        deletion_freeze()
    elif deletion == 'RESTART':
        print('=====Dictionary updated!======')
        dictionary = deletion_restart(dictionary, 'decompress')
    elif deletion == 'LRU':
        deletion_LRU()
    return dictionary
    




def compressor(data, dictionary,update_method, deletion):
    n = len(data)
    compress_result = []
    head = 0
    tail = 1
    prev = ''
    while tail <= n:
        while data[head:tail] in dictionary and tail <= n:
            tail += 1
        current_match = data[head:tail-1]
        compress_result.append(dictionary[current_match])
        if update_method == 'FC':
            update = prev + current_match[0]
        elif update_method == 'CM':
            update = prev + current_match
        else:
            print('Sorry %s is not supported'%update_method)
            return None
        dictionary = update_dict(dictionary, update, deletion)
        prev = current_match
        head = tail -1
        tail = head + 1
    
    return compress_result


def decompressor(code, dictionary, update_method, deletion):
    decompress_result = ""
    prev = ""
    # n = len(code)
    # idx = 0
    # each = n//5
    for num in code:
        current = dictionary[num]
        decompress_result += current
        if update_method == 'FC':
            update = prev + current[0]
        elif update_method == 'CM':
            update = prev + current
        else:
            print('Sorry %s is not supported'%update_method)
            return None
        dictionary = update_dict_decompress(dictionary, update, deletion)
        prev = current
        # idx += 1
        # if idx%each == 0:
        #     embed()
        
    return decompress_result





    


class Compressor():

    def __init__(self,filepath, method = 'FC', deletion = 'FREEZE', data = None, outpath = 'results'):
        try:
            with open(filepath,'r') as f:
                self.datasetname = filepath.rsplit('/',1)[-1].split('.')[0]
                self.data = f.read()
        except IOError:
            print("File is not accessible.")
        if data:
            self.data = data

        self.method = method
        self.deletion = deletion
        self.outpath = outpath
    
    def compress(self):
        dictionary = dict((chr(x), x) for x in range(128))
        self.compress_result = compressor(self.data, dictionary, self.method, self.deletion)

    def decompress(self):
        dictionary = dict((x,chr(x)) for x in range(128))
        self.decompress_result = decompressor(self.compress_result, dictionary, self.method, self.deletion)
        print("The decompression result of %s update and %s deletion equals the origin text: "%(self.method,self.deletion),self.decompress_result == self.data)

    def export_compress_result(self):
        filename = self.datasetname + '-encode-' + str(round(time.time())) + '.txt'
        path = os.path.join(self.outpath,filename)
        with open(path, 'w') as f:
            f.write(str(self.compress_result))
    
    def export_decompress_result(self):
        filename = self.datasetname + '-decode-' + str(round(time.time())) + '.txt'
        path = os.path.join(self.outpath,filename)
        with open(path, 'w') as f:
            f.write(str(self.decompress_result))

            






    
        

        
