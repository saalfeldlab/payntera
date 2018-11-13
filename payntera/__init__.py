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
    RELEVANT_MAVEN_REPOS = {
                'imagej.public' : 'https://maven.imagej.net/content/groups/public',
                'saalfeldlab'   : 'https://saalfeldlab.github.io/maven'
    }
    for _, repo in scyjava_config.get_repositories().items():
        if 'imagej.public' in RELEVANT_MAVEN_REPOS and repo == RELEVANT_MAVEN_REPOS['imagej.public']:
            del RELEVANT_MAVEN_REPOS['imagej.public']
        if 'saalfeldlab' in RELEVANT_MAVEN_REPOS and repo == RELEVANT_MAVEN_REPOS['saalfeldlab']:
            del RELEVANT_MAVEN_REPOS['saalfeldlab']

    scyjava_config.add_endpoints(PAINTERA_ENDPOINT, '{}'.format(os.getenv('PAINTERA_SLF4J_BINDING', 'org.slf4j:slf4j-simple:1.7.25')))
    scyjava_config.add_repositories(RELEVANT_MAVEN_REPOS)

    scyjava_config.add_classpath(_jfx_rt_jar)

    return scyjava_config

scyjava_config = _init_jvm_options()


