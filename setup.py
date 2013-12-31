#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='insol',
      version='2.0.1',
      description='Solr search server API for python',
      author='Michael Domanski',
      author_email='mdomans@gmail.com',
      packages=find_packages(),
      license='Apache 2.0',
      install_requires = ['requests>=2.1.0'],
      classifiers=[
          'Environment :: Console',
          'Environment :: Web Environment',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],
     )