__author__ = 'jnduan'
import codecs
import json
import os
import re
input_files = os.listdir('../output')
train_fp = codecs.open('../output/predict', 'w', 'utf-8')
for input_file in input_files:
    if input_file.startswith('xditems_attrs_'):
        print 'process %s' %(input_file)
        fp = codecs.open('../output/'+input_file, 'rU', 'utf-8')
        for line in fp:
            obj = json.loads(line, 'utf-8')
            for k in obj.keys():
                train_fp.write(k.replace(' ', ''))
                train_fp.write('\t')
                train_fp.write(obj[k])
                train_fp.write('\r\n')
        fp.close()

train_fp.close()