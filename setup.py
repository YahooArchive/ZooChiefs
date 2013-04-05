#!/usr/bin/env python

import os

import setuptools

from chief import version


def get_version():
    return str(version.version_string())


def read_requires():
    requires = []
    with open('tools/pip-requires', 'r') as fh:
        contents = fh.read()
        for line in contents.splitlines():
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            try:
                (line, after) = line.split("#", 1)
            except ValueError:
                pass
            if not line:
                continue
            requires.append(line)
    return requires


setuptools.setup(name='chief',
                 description='A cross system process leadership system',
                 author="Y! OpenStack Team",
                 packages=setuptools.find_packages(exclude=['tests']),
                 long_description=open('README.md').read(),
                 license='Apache License, Version 2.0',
                 version=get_version(),
                 scripts=['bin/solo.py'],
                 install_requires=read_requires())
