#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

from koalemos.koalemos import Koalemos

requires = [
    'Flask>=0.10.1'
]

setup(
    name='koalemos',
    description='',
    version=Koalemos.VERSION,
    packages=find_packages(),
    author='Peer Xu',
    author_email='pppeerxu@gmail.com',
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'koalemos-server=koalemos.server:main',
            'koalemos-client=koalemos.client:main'
        ]
    }
)
