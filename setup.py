import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="python-forecastio",
    version="1.3.2",
    author="Ze'ev Gilovitz",
    author_email="zeev.gil@gmail.com",
    description=("A thin Python Wrapper for the Forecast.io weather API"),
    license="BSD 2-clause",
    keywords="weather API wrapper forecast.io location",
    url="http://zeevgilovitz.com/python-forecast.io/",
    packages=['forecastio'],
    package_data={'forecastio': ['LICENSE.txt', 'README.rst']},
    long_description=open('README.rst').read(),
    install_requires=['requests>=1.6'],
)
