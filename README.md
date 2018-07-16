# Payntera

Python bindings for [Paintera](https://paintera.org)

## Installation

Install dependencies from conda:
```shell
conda install -c hanslovsky python=3.6 numpy jrun
```

Payntera cannot be distributed through conda currently because there is no openjfx package on conda. Instead, you will have to install some of the dependencies manually:

### OpenJDK and OpenJFX
On Arch Linux:
```shell
pacman -S jdk8-openjdk java-openjfx
# set JAVA_HOME environment variable:
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk
```

### PyJNIus
(tested on Linux)
```shell
# make sure that JAVA_HOME is set, e.g.
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk
git clone git@github.com:kivy/pyjnius.git
cd pyjnius
make
make tests
pip install .
# set PYJNIUS_JAR environment variable:
export PYJNIUS_JAR=$PWD/build/pyjnius.jar
```

### ImgLyb
```shell
git clone git@github.com:hanslovsky/imglyb
cd imglyb
pip install .
```

### Payntera
```shell
git clone git@github.com:saalfeldlab/payntera
cd payntera
pip install .
```

## Usage
Make sure that `JAVA_HOME` and `PYJNIUS_JAR` environemnt variables are set (see [Installation](https://github.com/saalfeldlab/payntera#Installation)).
**Always** respect this order of imports:
```python
import payntera
import imglyb
from jnius import ...
```

Example usage:
```python
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

max_id = 30
arr    = np.random.randint(max_id - 1, size=(300,200,100)) + 1
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

raw           = np.zeros(arr.shape, dtype=np.uint8)
raw[arr > max_id // 2] = 255
raw_img       = imglyb.to_imglib(raw)

raw_state = RawSourceState.simpleSourceFromSingleRAI(
    raw_img,
    [1.0, 1.0, 1.0],
    [0.0, 0.0, 0.0],
    0.0,
    255.0,
    'blub'
    )

payntera.jfx.invoke_on_jfx_application_thread( lambda : viewer.baseView.addRawSource( raw_state ) )
payntera.jfx.invoke_on_jfx_application_thread( lambda : viewer.baseView.addLabelSource( state ) )

viewer.keyTracker.installInto(scene)
scene.addEventFilter(autoclass('javafx.scene.input.MouseEvent').ANY, viewer.mouseTracker)


# Keep Python alive (Python is unaware of Java threads).

while True:
    time.sleep(0.5)
```
