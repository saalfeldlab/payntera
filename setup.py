import setuptools

version={}
with open('payntera/version.py', 'r') as f:
    exec(f.read(), version)

setuptools.setup(
    name='payntera',
    version=version['__version__'],
    author='Philipp Hanslovsky',
    author_email='hanslovskyp@janelia.hhmi.org',
    description='Python convenience bindings for Paintera',
    packages=['payntera'],
    install_requires=['numpy', 'pyjnius', 'jrun', 'imglyb']
)
