# -*- coding: utf-8 -*-
# Learn more: https://github.com/kennethreitz/setup.py
from setuptools import setup, find_packages

# Version numbering scheme, see
# https://packaging.python.org/distributing/#choosing-a-versioning-scheme
# 1.2.0.dev1  # Development release
# 1.2.0a1     # Alpha Release
# 1.2.0b1     # Beta Release
# 1.2.0rc1    # Release Candidate
# 1.2.0       # Final Release
# 1.2.0.post1 # Post Release
__version__ = '0.0.1.dev1'


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cosycar',
    version=__version__,
    description='Keep your car cosy with heaters and Vera',
    long_description=readme,
    author='Mats Gustafsson',
    author_email='e-contact@mats-gustafsson.se',
    url='https://github.com/eragnms/cosycar',
    license=license,
    entry_points={
        'console_scripts': [
            'cosycar = cosycar.cosycar:main'
            ]
    },
    packages=['cosycar'],
    install_requires=[
        '',
    ],
)

