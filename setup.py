# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    # Note that README is not in *.rst
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='webreg-to-cal',
    version='0.1.0',
    description='Adds class schedule to Google Calendar',
    long_description=readme,
    author='Zixuan Rao',
    author_email='z1rao@ucsd.edu',
    url='https://github.com/div-e/webreg-to-cal',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

