# -*- coding: utf-8 -*-
# Learn more: https://github.com/kennethreitz/setup.py
from cosycar.__main__ import __version__

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cosy-car',
    version=__version__,
    description='Keep your car cosy with heaters and Vera',
    long_description=readme,
    author='Mats Gustafsson',
    author_email='e-contact@mats-gustafsson.se',
    url='https://github.com/eragnms/cosy-car',
    license=license,
    entry_points={
        'console_scripts': [
            'cosycar = cosycar.__main__:main'
            ]
    },
    packages=find_packages(exclude=('tests', 'docs'))
)

