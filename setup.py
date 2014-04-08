from setuptools import setup

setup(
    name='LumixMaptool',
    version='1.0.11',
    author='Martin Thoma',
    author_email='info@martin-thoma.de',
    packages=['lumixmaptool'],
    scripts=['lumixmaptool/lumixmaptool.py'],
    url='https://github.com/MartinThoma/lumix_map_tool',
    license='LICENSE',
    description='Manage GPS information for Panasonic Lumix cameras.',
    long_description="""Panasonic offers GPS metadata to add to a SD card. This metadata can contain
tourist information that might be useful for sightseeing. This maptool helps
to copy the data from Lumix DVD to the SD card that is inserted into your 
computer (the camera has not to be connected).""",
    install_requires=[
        "argparse >= 1.2.1",
        "pyparsing >= 2.0.1",
        "pyparsing >= 2.0.1",
    ],
    entry_points={
        'console_scripts':
            ['lumixmaptool = lumixmaptool:main']
    }
)