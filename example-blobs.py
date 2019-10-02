# set heap size to reasonable value
import jnius_config
jnius_config.add_options('-Xmx8g')

import numpy as np
import payntera
import payntera.jfx
import scipy.ndimage
import time

import imglyb
viewer = payntera.start_paintera_viewer()

shape      = (80,80,50)
x, y, z    = np.indices(shape)
fx, fy, fz = 2 * np.pi / np.array(shape) * np.array([10, 1, 3])
raw        = (1+np.sin(x * fx)) * (1+np.sin(y * fy)) * (1+x*y/(shape[0]*shape[1]))**2 * (1+np.cos(z * fz)) * ((x+y+z)/np.sum(shape))
labels, nb = scipy.ndimage.label(raw > 0.5)

viewer.add_raw(data=raw, name='blub', minv=np.min(raw), maxv=8)
viewer.add_labels(data=labels, name='bla', max_id=nb+1)

while viewer.isShowing():
    time.sleep(0.1)
