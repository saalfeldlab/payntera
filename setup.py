import os
import glob
from subprocess import call
from distutils.core import setup
from distutils.command.build_py import build_py

version={}
with open('payntera/version.py', 'r') as f:
    exec(f.read(), version)

setup(
    name='payntera',
    version=version['__version__'],
    author='Philipp Hanslovsky',
    author_email='hanslovskyp@janelia.hhmi.org',
    description='Python convenience bindings for Paintera',
    packages=['payntera'],
    install_requires=['numpy', 'pyjnius', 'jrun', 'imglyb']
)
