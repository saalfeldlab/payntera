import dask.array
import numpy as np
import payntera
import payntera.jfx
import time

# imglyb and jnius must be imported after payntera is imported!
import imglyb
import imglyb.cell
# jnius must be imported after imglyb is imported!
from jnius import autoclass, JavaException


payntera.jfx.init_platform()
PainteraBaseView = autoclass('org.janelia.saalfeldlab.paintera.PainteraBaseView')
try:
    viewer           = PainteraBaseView.defaultView()
except JavaException as e:
    print(e)
    print("inner message", e.innermessage)
    if e.stacktrace:
        for l in e.stacktrace:
            print(l)
    raise e

scene, stage = payntera.jfx.start_stage(viewer.paneWithStatus.getPane())

LabelSourceState = autoclass('org.janelia.saalfeldlab.paintera.state.LabelSourceState')
RawSourceState   = autoclass('org.janelia.saalfeldlab.paintera.state.RawSourceState')

chunks   = (64, 64, 64)
max_id   = 30
arr      = np.random.randint(max_id - 1, size=(300,200,100)) + 1
dask_arr = dask.array.from_array(arr, chunks=chunks).rechunk(chunks)
img      = imglyb.cell.dask_array_as_cached_cell_img(dask_arr, volatile_access=True)


state = LabelSourceState.simpleSourceFromSingleRAI(
    img,
    [1.0, 1.0, 1.0],
    [0.0, 0.0, 0.0],
    max_id,
    'bla',
    viewer.baseView.viewer3D().meshesGroup(),
    viewer.baseView.getMeshManagerExecutorService(),
    viewer.baseView.getMeshWorkerExecutorService()
    )

raw                    = np.zeros(arr.shape, dtype=np.uint8)
raw[arr > max_id // 2] = 255
dask_raw               = dask.array.from_array(raw, chunks=chunks).rechunk(chunks)
raw_img                = imglyb.cell.dask_array_as_cached_cell_img(dask_raw, volatile_access=True)

raw_state = RawSourceState.simpleSourceFromSingleRAI(
    raw_img,
    [1.0, 1.0, 1.0],
    [0.0, 0.0, 0.0],
    0.0,
    255.0,
    'blub'
    )

viewer.keyTracker.installInto(scene)
scene.addEventFilter(autoclass('javafx.scene.input.MouseEvent').ANY, viewer.mouseTracker)

payntera.jfx.invoke_on_jfx_application_thread( lambda : viewer.baseView.addRawSource( raw_state ) )
# payntera.jfx.invoke_on_jfx_application_thread( lambda : viewer.baseView.addLabelSource( state ) )



while True:
    time.sleep(0.5)

