import payntera
import payntera.jfx
import time
import traceback


from jnius import autoclass, JavaException


PainteraBaseView = autoclass('org.janelia.saalfeldlab.paintera.PainteraBaseView')
try:
    viewer           = PainteraBaseView.defaultView()
except JavaException as e:
    print(e)
    print("inner message", e.innermessage)
    raise e

payntera.jfx.init_platform()
print(dir(viewer))
payntera.jfx.start_stage(viewer.baseView.pane())

while True:
    time.sleep(0.5)

