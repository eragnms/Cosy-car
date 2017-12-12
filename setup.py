# -*- coding: utf-8 -*-
# Learn more: https://github.com/kennethreitz/setup.py
import re
import io
import os
from setuptools import setup, find_packages


def read(*names, **kwargs):
    with io.open(
            os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cosycar',
    version=find_version("cosycar/cosycar.py"),
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
        'pyvera',
        'urllib3',
        'json',
    ],
    data_files=[(os.environ['HOME'] + '/.config',
                 ['cosycar/config/cosycar_template.cfg'])],
)

