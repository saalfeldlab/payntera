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

Usage example ([`example-blobs.py`](https://github.com/saalfeldlab/payntera/blob/3f28f130c4eaf4e3f62ca9fd110b91af9092f1d4/example-blobs.py)):
```python
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
```
