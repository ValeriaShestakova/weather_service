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
    name='WeatherService',
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
    install_requires=['flask', 'psycopg2', 'flask-restful', 'pyyaml', 'requests', 'grequests'],
    extras_require={
        'dev': ['pytest', 'pylint'],
        },
    test_suite='tests'

)
