import h5py
import numpy as np
import os
import pathlib
import payntera
import payntera.jfx
import time

# imglyb and jnius must be imported after payntera is imported!
import imglyb
# jnius must be imported after imglyb is imported!
from jnius import autoclass, JavaException

import os

cremi_file = os.getenv('CREMI_FILE', os.path.join(pathlib.Path.home(), 'Downloads', 'sample_A_20160501.hdf'))

payntera.jfx.init_platform()
PainteraBaseView = autoclass('org.janelia.saalfeldlab.paintera.PainteraBaseView')
viewer           = PainteraBaseView.defaultView()
scene, stage     = payntera.jfx.start_stage(viewer.paneWithStatus.getPane())

LabelSourceState = autoclass('org.janelia.saalfeldlab.paintera.state.LabelSourceState')
RawSourceState   = autoclass('org.janelia.saalfeldlab.paintera.state.RawSourceState')

with h5py.File(cremi_file, 'r') as f:
    raw_dataset        = f['volumes/raw']
    neuron_ids_dataset = f['volumes/labels/neuron_ids']
    raw_res            = [x for x in raw_dataset.attrs['resolution'][::-1]] if 'resolution' in raw_dataset.attrs else [1.0, 1.0, 1.0]
    raw_off            = [x for x in raw_dataset.attrs['offset'][::-1]] if 'offset' in raw_dataset.attrs else [1.0, 1.0, 1.0]
    neuron_ids_res     = [x for x in neuron_ids_dataset.attrs['resolution'][::-1]] if 'resolution' in neuron_ids_dataset.attrs else [1.0, 1.0, 1.0]
    neuron_ids_off     = [x for x in neuron_ids_dataset.attrs['offset'][::-1]] if 'offset' in neuron_ids_dataset.attrs else [1.0, 1.0, 1.0]
    raw                = raw_dataset.value
    neuron_ids         = neuron_ids_dataset.value

max_id = np.max(neuron_ids) + 1
img    = imglyb.to_imglib(neuron_ids)
state  = LabelSourceState.simpleSourceFromSingleRAI(
    img,
    neuron_ids_res,
    neuron_ids_off,
    max_id,
    'neuron ids',
    viewer.baseView.viewer3D().meshesGroup(),
    viewer.baseView.getMeshManagerExecutorService(),
    viewer.baseView.getMeshWorkerExecutorService()
    )

raw_img   = imglyb.to_imglib(raw)
raw_state = RawSourceState.simpleSourceFromSingleRAI(
    raw_img,
    raw_res,
    raw_off,
    0.0,
    255.0,
    'raw'
    )

viewer.keyTracker.installInto(scene)
scene.addEventFilter(autoclass('javafx.scene.input.MouseEvent').ANY, viewer.mouseTracker)

payntera.jfx.invoke_on_jfx_application_thread( lambda : viewer.baseView.addRawSource( raw_state ) )
payntera.jfx.invoke_on_jfx_application_thread( lambda : viewer.baseView.addLabelSource( state ) )


# Keep Python alive (Python is unaware of Java threads).

while True:
    time.sleep(0.5)

