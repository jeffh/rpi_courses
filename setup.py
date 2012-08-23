#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='RPICourses',
    description=md.__description__,
    license='MIT',
    version='1.0.0',
    author='Jeff Hui',
    author_email='jeff@jeffhui.net',
    url='https://github.com/jeffh/rpi_courses',
    packages=find_packages(),
    requires=[
        'BeautifulSoup',
    ],
    long_description=open('README.rst').read(),
    test_suite=['rpi_courses.tests'],
    test_requires=[
        'mock',
        'nose',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable' # I wish
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
    ],
)
