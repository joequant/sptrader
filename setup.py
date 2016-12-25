#!/usr/bin/env python3

from distutils.core import setup

setup(name='sptrader',
      version='0.7.0',
      description='SharpPoint trading system',
      author='Joseph C Wang',
      author_email='joequant@gmail.com',
      url='https://github.com/joequant/sptrader',
      packages=['sptrader'],
      install_requires=[
    'cffi',
    'flask',
    'backtrader==1.9.12.99',
    'matplotlib',
    'sseclient-py',
    'requests',
    'pytz'
    ]
      )
