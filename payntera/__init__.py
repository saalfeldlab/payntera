from .version import __version__

import os

__paintera_version__ = os.getenv('PAINTERA_VERSION', __version__)
__jfx_rt_jar         = os.getenv('JFX_RT_JAR', os.path.join(os.getenv('JAVA_HOME'), 'jre', 'lib', 'ext', 'jfxrt.jar'))


def _init_jvm_options():

    import imglyb_config

    import jnius_config

    PAINTERA_ENDPOINT    = 'org.janelia.saalfeldlab:paintera:{}'.format(__paintera_version__)
    RELEVANT_MAVEN_REPOS = {
                'imagej.public' : 'https://maven.imagej.net/content/groups/public',
                'saalfeldlab'   : 'https://saalfeldlab.github.io/maven'
        }

    imglyb_config.add_endpoints(PAINTERA_ENDPOINT, '{}'.format(os.getenv('PAINTERA_SLF4J_BINDING', 'org.slf4j:slf4j-simple:1.7.25')))
    imglyb_config.add_repositories(RELEVANT_MAVEN_REPOS)

    JVM_OPTIONS_STR = 'JVM_OPTIONS'

    if JVM_OPTIONS_STR in os.environ:
            jnius_config.add_options( *os.environ[ JVM_OPTIONS_STR ].split(' ') )
                
    jnius_config.add_classpath(__jfx_rt_jar)

    return jnius_config

jnius_config = _init_jvm_options()


