from distutils.core import setup
import sys


if 'develop' in sys.argv:
    from setuptools import setup

setup(
    name='filedb',
    version='1.0',
    maintainer='Felix',
    maintainer_email='felix.marczinowski@blue-yonder.com',
    url='https://github.com/fmarczin/demo',
    packages=['filedb'],
)
