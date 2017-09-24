# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cosy-car',
    version='0.0.1',
    description='Keep your car cosy with heaters and Vera',
    long_description=readme,
    author='Mats Gustafsson',
    author_email='e-contact@mats-gustafsson.se',
    url='https://github.com/eragnms/cosy-car',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

