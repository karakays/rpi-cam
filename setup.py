#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='rpi_cam',
    version='0.1-:dev',
    url='https://github.com/karakays/rpi-cam',
    author=u'Selçuk Karakayalı',
    author_email='skarakayali@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask', 'flask_wtf', 'wtforms', 'gevent'
    ],
)
