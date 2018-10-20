from Compressor import Compressor
filepath = 'testfiles/news.txt'
# compressor = Compressor(filepath, data='baaaabaaabc', method='CM')
# compressor.compress()
# compressor.decompress()

# compressor2 = Compressor(filepath, data='baacaabasaab', method='FC')
# compressor2.compress()
# compressor2.decompress()


compressor = Compressor(filepath, method='CM')
compressor.compress()
compressor.export_compress_result()
compressor.decompress()


compressor2 = Compressor(filepath, method='FC')
compressor2.compress()
compressor2.decompress()


compressor = Compressor(filepath, method='CM')
compressor.compress()
#compressor.export_compress_result()
compressor.decompress()


compressor2 = Compressor(filepath, method='FC', deletion= 'RESTART')
compressor2.compress()
compressor2.decompress()

compressor2 = Compressor(filepath, method='FC', deletion= 'LRU')
compressor2.compress()
compressor2.decompress()