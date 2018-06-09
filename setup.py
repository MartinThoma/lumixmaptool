# Core modules
import io
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(os.path.join(os.path.dirname(__file__), file_name),
                 encoding='utf-8') as f:
        return f.read()

config = {
    'name': 'lumixmaptool',
    'version': '1.0.16',
    'author': 'Martin Thoma',
    'author_email': 'info@martin-thoma.de',
    'maintainer': 'Martin Thoma',
    'maintainer_email': 'info@martin-thoma.de',
    'packages': ['lumixmaptool'],
    'scripts': ['bin/lumixmaptool'],
    'platforms': ['Linux', 'MacOS X', 'Windows'],
    'url': 'https://github.com/MartinThoma/lumixmaptool',
    'license': 'MIT',
    'description': 'Manage GPS information for Panasonic Lumix cameras.',
    'long_description': read('README.md'),
    'long_description_content_type': 'text/markdown',
    'install_requires': [
        "argparse >= 1.2.1",
        "pyparsing >= 2.0.1",
        "pyparsing >= 2.0.1"
    ],
    'keywords': ['Lumix', 'Panasonic', 'TZ41', 'Camera', 'GPS'],
    'download_url': 'https://github.com/MartinThoma/lumixmaptool',
    'classifiers': ['Development Status :: 7 - Inactive',
                    'Environment :: Console',
                    'Intended Audience :: End Users/Desktop',
                    'License :: OSI Approved :: MIT License',
                    'Natural Language :: English',
                    'Operating System :: POSIX :: Linux',
                    'Programming Language :: Python',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.3',
                    'Programming Language :: Python :: 3.4',
                    'Topic :: Utilities'],
    'zip_safe': False,
    'test_suite': 'nose.collector'
}

setup(**config)
