import tomosaic
import tomopy
import glob, os
import numpy as np
import pickle
import dxchange
try:
    from mosaic_meta import *
except:
    reader = open(os.path.join('tomosaic_misc', 'meta'), 'rb')
    prefix, file_grid, x_shift, y_shift = pickle.load(reader)
    reader.close()
from mosaic_util import *

# ==========================================
center_st = None
center_end = None
center_step = 1
row_st = 0
row_end = 1
method = 'manual' # 'manual' or 'vo'
mode = 'discrete' # 'discrete' or 'merged' or 'single'
in_tile_pos = 400
ds = 1
dest_folder = 'center'
# merged:
slice_no = 600
# discrete:
source_folder = 'data_raw_1x'
# merged:
fname = 'fulldata_flatcorr_1x/fulldata_flatcorr_1x.h5'
# single:
sino_name = 'sino_4810.tiff'
preprocess_single = False
# ==========================================

import time
import logging
from skimage.transform import resize as imresize
from tomosaic.center import *

logger = logging.getLogger(__name__)

try:
    shift_grid = tomosaic.util.file2grid("shifts.txt")
    shift_grid = tomosaic.absolute_shift_grid(shift_grid, file_grid)
except:
    print('Refined shift is not provided. Using pre-set shift values. ')
    shift_grid = tomosaic.start_shift_grid(file_grid, x_shift, y_shift)
print(shift_grid)

if center_st is None:
    pano_list = glob.glob(os.path.join('preview_panos', '*_norm.tiff'))
    pano_list.sort()
    img1 = dxchange.read_tiff(pano_list[0])
    img2 = dxchange.read_tiff(pano_list[-1])
    center_init = tomopy.find_center_pc(np.squeeze(img1), np.squeeze(img2))
    print('Phase correlation estimate: {}'.format(center_init))
    center_st = center_init - 5
    center_end = center_init + 5
    # write current center into center_pos.txt file
    np.savetxt('center_pos.txt', np.vstack([range(row_st, row_end), [center_init] * (row_end - row_st)]).transpose(), fmt=['%d', '%.1f'])

shift_grid = shift_grid / ds
in_tile_pos = in_tile_pos / ds

t0 = time.time()
if mode == 'merged':
    find_center_merged(fname, shift_grid, (row_st, row_end), (center_st, center_end), search_step=center_step, slice=slice_no,
                       method=method)
elif mode == 'discrete':
    find_center_discrete(source_folder, file_grid, shift_grid, (row_st, row_end), (center_st, center_end), center_step,
                         slice=in_tile_pos, method=method)
elif mode == 'single':
    find_center_single(sino_name, (center_st, center_end), center_step, preprocess_single=preprocess_single,
                       method=method)
print('Rank {}: total time = {} s.'.format(rank, time.time() - t0))
