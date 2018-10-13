from Compressor import Compressor
filepath = 'testfiles/bib.txt'
compressor = Compressor(filepath, data='abababac', method='NC')
compressor.compress()
