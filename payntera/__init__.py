import jnius_config
import os

__paintera_version__ = os.getenv('PAINTERA_VERSION' ,'0.2.0')
__jfx_rt_jar         = os.getenv('JFX_RT_JAR', os.path.join(os.getenv('JAVA_HOME'), 'jre', 'lib', 'ext', 'jfxrt.jar'))


def _init_jvm_options():

    import jnius_config

    import jrun.jrun
    

    PAINTERA_ENDPOINT    = 'org.janelia.saalfeldlab:paintera:{}'.format(__paintera_version__)
    PYJNIUS_JAR_STR      = 'PYJNIUS_JAR'
    IMGLYB_JAR_CACHE_DIR = os.path.join(os.getenv('HOME'), '.imglyb-jars')
    LOCAL_MAVEN_REPO     = os.getenv('M2_REPO', os.path.join(os.getenv('HOME'), '.m2', 'repository'))
    RELEVANT_MAVEN_REPOS = {
                'imagej.public' : 'https://maven.imagej.net/content/groups/public',
                'saalfeldlab'   : 'https://saalfeldlab.github.io/maven'
        }

    paintera_jars = jrun.jrun.resolve_dependencies(
        endpoint     = PAINTERA_ENDPOINT,
        cache_dir    = IMGLYB_JAR_CACHE_DIR,
        m2_repo      = LOCAL_MAVEN_REPO,
        repositories = RELEVANT_MAVEN_REPOS,
        verbose      = 0
        )

    logging_jars = jrun.jrun.resolve_dependencies(
        endpoint     = '{}'.format(os.getenv('PAINTERA_SLF4J_BINDING', 'org.slf4j:slf4j-simple:1.7.25')),
        cache_dir    = IMGLYB_JAR_CACHE_DIR,
        m2_repo      = LOCAL_MAVEN_REPO,
        repositories = RELEVANT_MAVEN_REPOS,
        verbose      = 0
        )

    for jar in paintera_jars + logging_jars:
        jnius_config.add_classpath(jar)

    JVM_OPTIONS_STR = 'JVM_OPTIONS'

    if JVM_OPTIONS_STR in os.environ:
            jnius_config.add_options( *os.environ[ JVM_OPTIONS_STR ].split(' ') )
                
    jnius_config.add_classpath(__jfx_rt_jar)

    if PYJNIUS_JAR_STR not in globals():
        try:
            PYJNIUS_JAR=os.environ[ PYJNIUS_JAR_STR ]
        except KeyError as e:
            print( "Path to pyjnius.jar not defined! Use environment variable {} to define it.".format( PYJNIUS_JAR_STR ) )
            raise e

    jnius_config.add_classpath(PYJNIUS_JAR)

    return jnius_config

jnius_config = _init_jvm_options()


