import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "python-forecastio",
    version = "0.1",
    author = "Ze'ev Gilovitz",
    author_email = "zeev.gil@gmail.com",
    description = ("A thin Python Wrapper for the Forecast.io weather API"),
    license = "BSD 2-clause",
    keywords = "weather API wrapper forecast.io location",
    url = "https://github.com/ZeevG/python-forcast.io",
    packages=['forecastio'],
    package_data={'forecastio': ['LICENSE.txt', 'README.md']},
    long_description=read('README.md'),
    install_requires=['requests'],
)
