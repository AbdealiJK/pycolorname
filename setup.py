#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import pycolorname

with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

with open('test-requirements.txt') as requirements:
    test_required = requirements.read().splitlines()

if __name__ == "__main__":
    setup(name='pycolorname',
          version=pycolorname.__version__,
          description='Provides common color systems.',
          author="DrTrigon",
          author_email="dr.trigon@surfeu.ch",
          maintainer="AbdealiJK",
          maintainer_email='abdealikothari@gmail.com',
          url='https://github.com/AbdealiJK/pycolorname',
          platforms='any',
          packages=find_packages(exclude=["build.*", "*.tests.*", "*.tests"]),
          install_requires=required,
          tests_require=test_required,
          license="MIT",
          package_data={'pycolorname': ["VERSION", "data/*"]},
          # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Console',
              'Environment :: MacOS X',
              'Environment :: Win32 (MS Windows)',
              'Intended Audience :: Developers',
              'Operating System :: OS Independent',
              'Programming Language :: Python :: Implementation :: CPython'])
