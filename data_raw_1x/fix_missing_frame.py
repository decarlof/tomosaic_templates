import numpy as np
import h5py
from shutil import copyfile
import os

supposed_nframes = 1500

fname = 'BYU304U_Sam12_TopHAZ_y2_x3.h5'
copyfile(fname, os.path.basename(os.path.splitext(fname)[0]) + '_bk.h5')
f = h5py.File(fname, 'r+')
grp = f['exchange']
dat = f['exchange/data']
a = dat[...]
actual_nframes = a.shape[0]
nframes_missing = supposed_nframes - actual_nframes
b = np.zeros([supposed_nframes, *a.shape[1:]], dtype=a.dtype)
b[:actual_nframes, :, :] = a
b[-nframes_missing, :, :] = a[-nframes_missing, :, :]
del f['exchange/data']
dat = grp.create_dataset('data', b.shape, dtype=a.dtype)
dat[...] = b

f.close()
