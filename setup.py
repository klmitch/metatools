#!/usr/bin/env python

from setuptools import setup


def readreq(filename):
    with open(filename) as f:
        reqs = [r.partition('#')[0].strip() for r in f]
        return [r for r in reqs if r]


def readfile(filename):
    with open(filename) as f:
        return f.read()


setup(
    name='Metatools',
    version='0.1.1',
    author='Kevin L. Mitchell',
    author_email='klmitch@mit.edu',
    url='http://github.com/klmitch/metatools/',
    description='Python Metaclass Construction Tools',
    long_description=readfile('README.rst'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    py_modules=['metatools'],
    tests_require=readreq('test-requires'),
    )
