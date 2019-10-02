from .version import __version__

import os

_paintera_version = os.getenv('PAINTERA_VERSION', __version__)
_jfx_rt_jar       = os.getenv('JFX_RT_JAR', os.path.join(os.getenv('JAVA_HOME'), 'jre', 'lib', 'ext', 'jfxrt.jar'))

assert os.path.exists(_jfx_rt_jar) and os.path.isfile(_jfx_rt_jar), 'JavaFX runtime jar does not exist ' \
                                                                    'at default location %s. Please specify ' \
                                                                    'JFX_RT_JAR environment variable.'


def _init_jvm_options():

    import scyjava_config

    PAINTERA_ENDPOINT    = 'org.janelia.saalfeldlab:paintera:{}'.format(_paintera_version)
    RELEVANT_MAVEN_REPOS = {'scijava.public' : 'https://maven.scijava.org/content/groups/public'}
    for _, repo in scyjava_config.get_repositories().items():
        if 'scijava.public' in RELEVANT_MAVEN_REPOS and repo == RELEVANT_MAVEN_REPOS['scijava.public']:
            del RELEVANT_MAVEN_REPOS['scijava.public']

    scyjava_config.add_endpoints(PAINTERA_ENDPOINT, '{}'.format(os.getenv('PAINTERA_SLF4J_BINDING', 'org.slf4j:slf4j-simple:1.7.25')))
    scyjava_config.add_repositories(RELEVANT_MAVEN_REPOS)

    scyjava_config.add_classpath(_jfx_rt_jar)

    return scyjava_config

scyjava_config = _init_jvm_options()

def start_paintera_viewer(project_directory = None):
    import imglyb
    from jnius import autoclass, cast
    from .jfx import \
     _get_invoke_on_jfx_application_thread, \
     _get_runnable, \
     init_platform, \
     start_stage

    init_platform()

    File               = autoclass('java.io.File')
    MouseEvent         = autoclass('javafx.scene.input.MouseEvent')
    PainteraMainWindow = autoclass('org.janelia.saalfeldlab.paintera.PainteraMainWindow')
    PainteraAlerts     = autoclass('org.janelia.saalfeldlab.paintera.ui.PainteraAlerts')
    mainWindow         = PainteraMainWindow()

    def func():
        if (not PainteraAlerts.ignoreLockFileDialog(mainWindow.projectDirectory, project_directory, "_Quit", False)):
            return None

        mainWindow.deserialize()

        scene, stage = start_stage(mainWindow.getPane())
        print("WAT ", scene, stage)
        mainWindow.setupStage(cast('javafx.stage.Stage', stage))
        mainWindow.pane.getScene().addEventFilter(MouseEvent.ANY, mainWindow.getMouseTracker())

    jfx_application_thread = _get_invoke_on_jfx_application_thread()
    jfx_application_thread.invokeAndWait(_get_runnable(func))

    return Payntera(mainWindow)

class Payntera(object):

    def __init__(self, mainWindow):
        super(Payntera, self).__init__()
        self.mainWindow = mainWindow
        self._baseView  = self.mainWindow.getBaseView()

    def add_raw(
            self,
            data,
            name,
            resolution = [1.0] * 3,
            offset = [0.0] * 3,
            minv = 0.0,
            maxv = 1.0):
        import imglyb
        from .jfx import invoke_on_jfx_application_thread

        img = imglyb.to_imglib(data)
        invoke_on_jfx_application_thread(lambda: self._add_raw(img, resolution, offset, minv, maxv, name))

    def _add_raw(self, img, resolution, offset, minv, maxv, name):
        self._baseView.addSingleScaleRawSource(img, resolution, offset, minv, maxv, name)

    def add_labels(
            self,
            data,
            name,
            max_id,
            resolution = [1.0] * 3,
            offset = [0.0] * 3):
        import imglyb
        from .jfx import invoke_on_jfx_application_thread

        img = imglyb.to_imglib(data)
        invoke_on_jfx_application_thread(lambda: self._add_labels(img, resolution, offset, max_id, name))

    def _add_labels(self, img, resolution, offset, max_id, name):
        self._baseView.addSingleScaleLabelSource(img, resolution, offset, max_id, name)


    def isShowing(self):
        return self.mainWindow.getPane().getScene().getWindow().isShowing()
