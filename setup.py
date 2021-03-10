#!/usr/bin/env python

from setuptools import setup

setup(
    name='target-mailgun',
    version='1.0.0',
    description='hotglue target for exporting data to email using the Mailgun API',
    author='hotglue',
    url='https://hotglue.xyz',
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    py_modules=['target_mailgun'],
    install_requires=[
        'requests==2.24.0',
        'argparse==1.4.0'
    ],
    entry_points='''
        [console_scripts]
        target-mailgun=target_mailgun:main
    ''',
    packages=['target_mailgun']
)
