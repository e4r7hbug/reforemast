#!/usr/bin/env python3
"""Reforemast installer."""
from setuptools import find_packages, setup

GITHUB_URL = 'https://github.com/e4r7hbug/reforemast'

setup(
    name='reforemast',
    description='Reformat Spinnaker Application and Pipeline configurations, change by change.',
    long_description='',
    author='',
    author_email='',
    url=GITHUB_URL,
    download_url=GITHUB_URL,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    setup_requires=['setuptools_scm'],
    use_scm_version={'local_scheme': 'dirty-tag'},
    install_requires=[
        'click',
        'pygments',
        'pyyaml',
        'requests',
    ],
    platforms=['OS Independent'],
    entry_points={
        'console_scripts': [
            'reforemast=reforemast.__main__:main',
        ],
    },
)
