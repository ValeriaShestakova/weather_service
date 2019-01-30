"""A setuptools based setup module.

"""
import os

from setuptools import setup, find_packages


def read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except FileNotFoundError:
        return ''


setup(
    name='Weather_service',
    version='0.1',
    description='Service to get weather data for SPb',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='',
    author='',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    extras_require={
        'dev': ['pytest', 'pylint'],
        },
    entry_points={
        'console_scripts': [
            'weather=WeatherAPI.__main__:main',
        ],
    },
    test_suite='tests'

)
