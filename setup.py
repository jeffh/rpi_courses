#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.rst') as handle:
    README = handle.read()

setup(
    name='RPICourses',
    description='A data scraping library to read course data from RPI.',
    license='MIT',
    version='1.0.4',
    author='Jeff Hui',
    author_email='jeff@jeffhui.net',
    url='https://github.com/jeffh/rpi_courses',
    packages=find_packages(),
    requires=[
        'BeautifulSoup',
        'pyPdf',
        'pyconstraints',
    ],
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable', # I wish
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
    ],
)
