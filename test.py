import numpy as np
import payntera
import payntera.jfx
import time
import traceback

import imglyb
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

arr    = np.random.randint(100,size=(300,200,100))
max_id = np.max(arr)
img    = imglyb.to_imglib(arr)


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

payntera.jfx.invoke_on_jfx_application_thread( lambda : viewer.baseView.addLabelSource( state ) )

viewer.keyTracker.installInto(scene)
scene.addEventFilter(autoclass('javafx.scene.input.MouseEvent').ANY, viewer.mouseTracker)



while True:
    time.sleep(0.5)

