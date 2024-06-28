#!/usr/bin/python
# coding:utf8

from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bayrol-poolaccess-mqtt',
    version="1.0.0",
    python_requires=">=3.11",
    packages=find_packages(exclude=['tests']),
    keywords=['bayrol', 'poolaccess', 'mqtt'],
    url='https://github.com/tdenolle/bayrol-poolaccess-mqtt',
    license='MIT',
    platforms=["any"],
    author='Tdenolle',
    author_email='thomas@denolle.fr',
    description='Easily connect Bayrol Poolaccess to Mqtt',
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=['paho.mqtt>=2.1.0,<3.0.0',
                      'requests>=2.1.0',
                      'docopt>=0.6.0,<1.0.0'],
    extras_require={
        'package': ["pep8", "flake8", "pep8-naming", "autopep8", "gitchangelog", "mako", ],
    },
    entry_points={
        'console_scripts': [
            'bayrol-poolaccess-mqtt=bayrol_poolaccess_mqtt.PoolaccessMqtt:main'
        ],
    },
    package_data={
        'data': ['sensors.json']
    }
)
