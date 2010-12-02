#!/usr/bin/env python
from setuptools import setup, find_packages
from rpi_courses import metadata as md

from rpi_courses.config import DEBUG

if DEBUG:
    raise TypeError, "Still in DEBUG mode, please set config.DEBUG = False"

setup(
    name='RpiCourses',
    description=md.__description__,
    license=md.__license__,
    version=md.__version__,
    author=md.__author__,
    author_email=md.__author_email__,
    url=md.__url__,
    packages=find_packages(),
    requires=[
        'BeautifulSoup',
    ],
    long_description=open('README.rst').read(),
    test_suite=['rpi_courses.tests'],
    test_requires=[
        'mock',
        'nose',
        'constraint',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable' # I wish
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
    ],
)