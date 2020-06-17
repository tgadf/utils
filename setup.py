from distutils.core import setup
import setuptools

setup(
  name = 'utils',
  py_modules = ['timeUtils', 'numpyUtils', 'pyUtils', 'sparkUtils', 'tsUtils', 'geoUtils', 'pandasUtils', 'tsneUtils', 'ioUtils', 'webUtils', 'fsUtils', 'searchUtils', 'uidUtils', 'fileUtils', 'strUtils', 'listUtils'],
  version = '0.0.1',
  description = 'General Utility Function',
  long_description = open('README.md').read(),
  author = 'Thomas Gadfort',
  author_email = 'tgadfort@gmail.com',
  license = "MIT",
  url = 'https://github.com/tgadf/utils',
  keywords = ['utilities'],
  classifiers = [
    'Development Status :: 3',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
  ],
  install_requires = ['numpy>=1.15.1', 'pandas>=0.23.4', 'matplotlib>=2.2.2', 'python-dateutil>=2.7.3', 'seaborn>=0.9.0', 'pyspark', 'bs4>=0.0.1']
)
