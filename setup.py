#!/usr/bin/env python
from setuptools import setup

setup(
    name='django-taggee',
    version='0.2',
    description='Tag field for Django models',
    keywords='django, tag, field',
    author='Dima Kurguzov',
    author_email='koorgoo@gmail.com',
    url='https://github.com/koorgoo/django-taggee/',
    license='MIT',
    packages=['taggee'],
    zip_safe=False,
    install_requires=[],
    include_package_delta=True,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Environment :: Web Environment'
    ],
)
