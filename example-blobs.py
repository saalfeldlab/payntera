# set heap size to reasonable value
import jnius_config
jnius_config.add_options('-Xmx2g')

import numpy as np
import payntera
import payntera.jfx
import scipy.ndimage
import time

# imglyb and jnius must be imported after payntera is imported!
import imglyb
# jnius must be imported after imglyb is imported!
from jnius import autoclass, JavaException

payntera.jfx.init_platform()

PainteraBaseView = autoclass('org.janelia.saalfeldlab.paintera.PainteraBaseView')
viewer           = PainteraBaseView.defaultView()
pbv              = viewer.baseView
scene, stage     = payntera.jfx.start_stage(viewer.paneWithStatus.getPane())

shape      = (80,80,50)
x, y, z    = np.indices(shape)
fx, fy, fz = 2 * np.pi / np.array(shape) * np.array([10, 1, 3])

raw        = (1+np.sin(x * fx)) * (1+np.sin(y * fy)) * (1+x*y/(shape[0]*shape[1]))**2 * (1+np.cos(z * fz)) * ((x+y+z)/np.sum(shape))
raw_img    = imglyb.to_imglib(raw)
labels, nb  = scipy.ndimage.label(raw > 0.5)
labels_img = imglyb.to_imglib(labels)


raw_state = pbv.addSingleScaleRawSource(raw_img, [1.0, 1.0, 1.0], [0.0, 0.0, 0.0], np.min(raw), 7, 'blub')
state     = pbv.addSingleScaleLabelSource(labels_img, [1.0, 1.0, 1.0], [0.0, 0.0, 0.0], nb+1, 'bla')

viewer.keyTracker.installInto(scene)
scene.addEventFilter(autoclass('javafx.scene.input.MouseEvent').ANY, viewer.mouseTracker)

while True:
    time.sleep(0.5)
