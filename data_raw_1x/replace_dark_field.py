import h5py
import numpy as np
from glob import glob
import os
import dxchange


flist = glob('*.h5')

for fname in flist:
    print(fname)
    f = h5py.File(fname, 'r+')
    dat = f['exchange/data_dark']
    dat[...] = 0
    f.close()
