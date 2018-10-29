def _get_class(qualified_name):
    from jnius import autoclass
    return autoclass(qualified_name)

def _get_platform_impl():
    return _get_class('com.sun.javafx.application.PlatformImpl')

def _get_jfx_util():
    return _get_class('org.janelia.saalfeldlab.fx.util.JFXUtil')

def _get_invoke_on_jfx_application_thread():
    return _get_class('org.janelia.saalfeldlab.fx.util.InvokeOnJavaFXApplicationThread')

def _get_scene():
    return _get_class('javafx.scene.Scene')

def _get_stage():
    return _get_class('javafx.stage.Stage')

def _get_platform():
    return _get_class('javafx.application.Platform')

def _get_runnable(func = lambda : None):
    from jnius import PythonJavaClass, java_method
    class _Runnable(PythonJavaClass):
        __javainterfaces__ = ['java/lang/Runnable']
        def __init__(self):
            super(_Runnable, self).__init__()

        @java_method('()V', name='run')
        def run(self):
            func()

    return _Runnable()

def _get_event_handler(func = lambda event : None):
    from jnius import PythonJavaClass, java_method
    class _EventHandler(PythonJavaClass):
        __javainterfaces__ = ['javafx.event.EventHandler']

        def __init__(self):
            super(_EventHandler, self).__init__()

        @java_method('(Ljavafx/event/Event;)V')
        def handle(self, event):
            return func(event)

    return _EventHandler()

def init_platform():
    import jnius
    from jnius import autoclass
    _get_jfx_util().platformImplStartup()

def start_stage(root):
    r = _get_runnable(lambda : _start_stage(root))
    jfx_application_thread = _get_invoke_on_jfx_application_thread()
    jfx_application_thread.invokeAndWait(r)
    scene = root.getScene()
    stage = root.getScene().getWindow()
    return scene, stage

def invoke_on_jfx_application_thread(func):
    _get_invoke_on_jfx_application_thread().invoke(_get_runnable(func))

def _start_stage(root):
    scene = _get_scene()(root)
    stage = _get_stage()()
    stage.setScene(scene)
    stage.show()
    
