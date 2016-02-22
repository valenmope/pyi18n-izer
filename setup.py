#!/usr/bin/env python
import os
import re
from setuptools import setup, find_packages

def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            # TODO support version numbers
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements

setup(
    name = 'pyi18n-izer',
    version = '0.1.0',
    description = "Python i18n tool for your app",
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    author = 'Valentin Moreno',
    author_email = 'valenmope@gmail.com',
    url = 'https://github.com/valenmope/pyi18n-izer',
    keywords = "Web frontend django",
    license = 'AGPLv3',
    packages = find_packages(exclude=('*.tests', '*.tests.*', 'tests.*', 'tests')),
    classifiers = (
        'Development Status :: 1 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ),
    zip_safe = True,
    install_requires=parse_requirements('requirements.txt'),
)
