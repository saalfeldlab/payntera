# Payntera

Python bindings for [Paintera](http://paintera.org)

## Installation

Payntera is availble as `payntera` on the conda channel `hanslovsky`.
After installation from conda
```shell
conda install -c hanslovsky -c conda-forge python=3.6 payntera
```
update your environment variables [`JAVA_HOME`](https://github.com/saalfeldlab/payntera#openjdk-and-openjfx) and [`PYJNIUS_JAR`](https://github.com/saalfeldlab/payntera#pyjnius-jar-file) to use your system Java and `pyjnius.jar` that was built against your system Java dynamic libraries. 
There is currently no JavaFX package on conda, and we cannot use OpenJDK from conda.
On Windows, you will most likely have to update `JDK_HOME` and `PATH`, as well.
All instructions are only tested on Linux.


### OpenJDK and OpenJFX
On Arch Linux (check your distribution's package manager for the correct packages):
```shell
pacman -S jdk8-openjdk java-openjfx
# set JAVA_HOME environment variable:
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk
```

### PyJNIus JAR File
(tested on Linux)
```shell
# make sure that JAVA_HOME is set, e.g.
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk
git clone git@github.com:kivy/pyjnius.git
cd pyjnius
make
make tests
# set PYJNIUS_JAR environment variable:
export PYJNIUS_JAR=$PWD/build/pyjnius.jar
```

## Usage
Make sure that `JAVA_HOME` and `PYJNIUS_JAR` environment variables are set (see [Installation](https://github.com/saalfeldlab/payntera#Installation)).
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

viewer.keyTracker.installInto(scene)
scene.addEventFilter(autoclass('javafx.scene.input.MouseEvent').ANY, viewer.mouseTracker)

payntera.jfx.invoke_on_jfx_application_thread( lambda : viewer.baseView.addRawSource( raw_state ) )
payntera.jfx.invoke_on_jfx_application_thread( lambda : viewer.baseView.addLabelSource( state ) )


# Keep Python alive (Python is unaware of Java threads).

while True:
    time.sleep(0.5)
```
