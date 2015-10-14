try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'lumixmaptool',
    'version': '1.0.15',
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
    'long_description': ("Panasonic offers GPS metadata to add to a SD card. "
                         "This metadata can contain tourist information that "
                         "might be useful for sightseeing. \n"
                         "This maptool helps to copy the data from Lumix DVD "
                         "to the SD card that is inserted into your computer "
                         "(the camera has not to be connected)."),
    'install_requires': [
        "argparse >= 1.2.1",
        "pyparsing >= 2.0.1",
        "pyparsing >= 2.0.1"
    ],
    'keywords': ['Lumix', 'Panasonic', 'TZ41', 'Camera', 'GPS'],
    'download_url': 'https://github.com/MartinThoma/lumixmaptool',
    'classifiers': ['Development Status :: 3 - Alpha',
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
