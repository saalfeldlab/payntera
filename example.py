# set heap size to reasonable value
import jnius_config
jnius_config.add_options('-Xmx2g')

import numpy as np
import payntera
import payntera.jfx
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

max_id = 30
arr    = np.random.randint(max_id - 1, size=(100,50,50)) + 1
img    = imglyb.to_imglib(arr)

raw                    = np.zeros(arr.shape, dtype=np.uint8)
raw[arr > max_id // 2] = 255
raw_img                = imglyb.to_imglib(raw)

raw_state = pbv.addSingleScaleRawSource(raw_img, [1.0, 1.0, 1.0], [0.0, 0.0, 0.0], 0.0, 255.0, 'blub')
state     = pbv.addSingleScaleLabelSource(img, [1.0, 1.0, 1.0], [0.0, 0.0, 0.0], max_id, 'bla')

viewer.keyTracker.installInto(scene)
scene.addEventFilter(autoclass('javafx.scene.input.MouseEvent').ANY, viewer.mouseTracker)

while True:
    time.sleep(0.5)
