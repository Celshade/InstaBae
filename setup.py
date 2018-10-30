"""Setup."""

from os import path
from setuptools import setup
from setuptools import find_packages

here = path.abspath(path.dirname(__file__))

# Meta Data
NAME = 'InstaBae'
DESCRIPTION = 'A way to automatically like bae\'s pictures.'
URL = 'https://github.com/Celshade/InstaBae'
EMAIL = 'ggcelshade@gmail.com'
AUTHOR = "Danny 'Celshade' Collins"
REQUIRES_PYTHON = '>=3.6'
VERSION = '0.0.4'
REQUIRES = ['selenium']
# TODO Include drivers in build.

# README handling
try:
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f'\n{f.read()}'
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRES,
    include_package_data=True,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GNU GPLv3 License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Terminal/Shell',
        'Intended Audience :: End Users/Desktop'
        'Intended Audience :: Developers', 'Users'
        'Topic :: Automation',
        'License :: OSI approved :: GNU GPLv3 License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.6'
        ],
    keywords='automation testing instagram InstaBae',
    project_urls={
        'Bug Reports': 'https://github.com/Celshade/InstaBae/bugs/2',
        'Comments': 'https://github.com/Celshade/InstaBae/issues/1',
        'Source': 'https://github.com/Celshade/InstaBae'
    }
)
