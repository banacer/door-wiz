# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Door-wiz',
    version='0.0.1',
    description='A door that uses ultrasonic sensors and ML to identify you based on your shape and walking behavior',
    long_description=readme,
    author='Nacer Khalil',
    author_email='nacerkhalil@gmil.com',
    url='https://github.com/banacer/door-wiz',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

