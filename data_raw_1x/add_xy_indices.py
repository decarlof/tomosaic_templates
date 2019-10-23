import numpy as np
from glob import glob
import os

n_x = 2
basename = glob('*.h5')[0][4:-3]

flist = glob('*.h5')
flist.sort()
if len(flist) % n_x != 0:
    raise ValueError('Number of files is not dividable by n_x!') 

rename_table = []
iy = 0
ix = 0
for f in flist:
    rename_entry = [f]
    new_name = basename + '_y{}_x{}.h5'.format(iy, ix)
    rename_entry.append(new_name)
    rename_table.append(rename_entry)
    ix += 1
    if ix == n_x:
        iy += 1
        ix = 0
print('Files will be named as follows:\n')
for i in range(len(rename_table)):
    print('{} -> {}'.format(rename_table[i][0], rename_table[i][1]))
print('\nProceed? (y/n):')
a = input()

if a in ['y', 'Y']:
    for i in range(len(rename_table)):
        os.rename(rename_table[i][0], rename_table[i][1])
else:
    print('Cancelled.')
