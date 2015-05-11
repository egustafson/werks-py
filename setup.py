#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name = "werks-py",
    version = "0.1",
    author = "Eric Gustafson",
    author_email = "ericg-git@elfwerks.org",
    license = "Apache Software License",
    packages = find_packages(exclude=['tmpapp']),
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: Apache Software License',
    ],
)
