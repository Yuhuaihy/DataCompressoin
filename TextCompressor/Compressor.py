import os
from IPython import embed
import time
import re
DICT_SIZE = 65536
class Node(object):
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


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

        self.unuse = []
        self.unuse2 = []
    
    def __init_dict(self, process):
        dictionary = {}
        self.head = Node(0,0)
        first = self.head
        self.string_set = set()
        for i in range(128):
            if process == 'encode':
                text = chr(i)
                code = bin(i)[2:].zfill(16)
            else:
                text = bin(i)[2:].zfill(16)
                code = chr(i)
                self.string_set.add(code)
            new = Node(text, code)
            if i == 0:
                self.tail = new
            first.next = new
            new.prev = first
            fisrt = first.next
            dictionary[text] = new
        return dictionary
    
    def __addNode(self, node):
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node
    
    def __removeNode(self, node):
        prev = node.prev
        prev.next = node.next
        node.next.prev = prev

    def update_dict(self, dictionary, key, deletion):
        if key in dictionary: 
            return dictionary
        
        if len(dictionary) < DICT_SIZE:
            code = bin(len(dictionary))[2:].zfill(16)
            new = Node(key, code)
            dictionary[key] = new
            self.__addNode(new)
            return dictionary
        
        if deletion == 'FREEZE':
            return dictionary

        elif deletion == 'RESTART':
            print('=====Dictionary updated!======')
            dictionary = self.__init_dict('encode')

        elif deletion == 'LRU':
            leastRecentUse = self.head.next
            k = leastRecentUse.key
            val = leastRecentUse.val
            new = Node(key, val)
            self.head.next = leastRecentUse.next
            leastRecentUse.next.prev = self.head
            dictionary.pop(k)
            self.__addNode(new)
            dictionary[key] = new
            
            
        return dictionary

    def update_dict_decompress(self, dictionary, value, deletion):
        if value in self.string_set:
            return dictionary
        n = len(dictionary)
        
        if len(dictionary) < DICT_SIZE:
            code = bin(n)[2:].zfill(16)
            new = Node(code, value)
            dictionary[code] = new
            self.__addNode(new)
            self.string_set.add(value)
            return dictionary
        if deletion == 'FREEZE':
            deletion_freeze()
        elif deletion == 'RESTART':
            print('=====Dictionary updated!======')
            dictionary = self.__init_dict('decode')
        elif deletion == 'LRU':
            
            leastRecentUse = self.head.next
            k = leastRecentUse.key
            val = leastRecentUse.val

            new = Node(k, value)

            self.head.next = leastRecentUse.next
            leastRecentUse.next.prev = self.head
            self.string_set.remove(val)
            self.__addNode(new)
            self.string_set.add(value)
            dictionary[k] = new



        return dictionary
        




    def compressor(self, data, dictionary,update_method, deletion):
        n = len(data)
        compress_result = ''
        head = 0
        tail = 1
        prev = ''
        while tail <= n:
            while data[head:tail] in dictionary and tail <= n:
                tail += 1
            current_match = data[head:tail-1]
            compress_result += dictionary[current_match].val

            if deletion == 'LRU' and len(current_match) > 1:
                node = dictionary[current_match]
                self.__removeNode(node)
                self.__addNode(node)

            if update_method == 'FC':
                update = prev + current_match[0]
            elif update_method == 'CM':
                update = prev + current_match
            else:
                print('Sorry %s is not supported'%update_method)
                return None
            dictionary = self.update_dict(dictionary, update, deletion)
            prev = current_match
            head = tail -1
            tail = head + 1
        
        return compress_result


    def decompressor(self, code, dictionary, update_method, deletion):
        decompress_result = ""
        prev = ""
        codes = re.findall(r'.{16}', code)
        for num in codes:
            current = dictionary[num].val
            decompress_result += current
            if deletion == 'LRU' and len(current)>1:
                node = dictionary[num]
                self.__removeNode(node)
                self.__addNode(node)

            if update_method == 'FC':
                update = prev + current[0]
            elif update_method == 'CM':
                update = prev + current
            else:
                print('Sorry %s is not supported'%update_method)
                return None
            dictionary = self.update_dict_decompress(dictionary, update, deletion)
            prev = current
            
            
        return decompress_result       
        
    def compress(self):
        dictionary = self.__init_dict('encode')
        self.compress_result = self.compressor(self.data, dictionary, self.method, self.deletion)

    def decompress(self):
        dictionary = self.__init_dict('decode')
        self.decompress_result = self.decompressor(self.compress_result, dictionary, self.method, self.deletion)
        print("The decompression result of %s update and %s deletion equals the origin text: "%(self.method,self.deletion),self.decompress_result == self.data)

    def export_compress_result(self):
        filename = self.datasetname + '-encode-' + str(round(time.time())) + '.txt'
        path = os.path.join(self.outpath,filename)
        with open(path, 'w') as f:
            f.write(self.compress_result)
    
    def export_decompress_result(self):
        filename = self.datasetname + '-decode-' + str(round(time.time())) + '.txt'
        path = os.path.join(self.outpath,filename)
        with open(path, 'w') as f:
            f.write(self.decompress_result)

            






    
        

        
