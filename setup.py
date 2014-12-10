#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

dev_requires = [
    "flake8>=2.2.0",
    "pytest>=2.6.0",
]

setup(
    name="Montanus",
    version="0.0.1",
    description="A tool for managing static files version for CDN requirements",
    author="Le Wang",
    author_email="le.wang@1tianxia.net",
    packages=["montanus", ],
    package_data={'montanus': ['montanus.conf.sample'], },
    entry_points={"console_scripts": ["montanus = montanus.cmd:main", ]},
    url="https://git.1tianxia.net/frontenddevops/montanus",
    license="MIT",
    long_description=open("README.md").read(),
    extras_require={
        "dev": dev_requires,
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ]
)
