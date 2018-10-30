from distutils.core import setup
import setuptools

setup(
  name = 'utils',
  py_modules = ['geohashUtils', 'numpyUtils', 'pandasUtils', 'pyUtils', 'sparkUtils', 'timeUtils', 'tsUtils', 'tsneUtils'],
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
  install_requires = ['pandas', 'numpy']
)
 


