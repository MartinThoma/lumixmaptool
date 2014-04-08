LumixMaptool
==============

Manage GPS information for Panasonic Lumix cameras.

Panasonic offers GPS metadata to add to a SD card. This metadata can contain
tourist information that might be useful for sightseeing. This maptool helps
to copy the data from Lumix DVD to the SD card that is inserted into your
computer (the camera has not to be connected).
This script was tested with Lumix TZ41.

## Usage

Install it:

```bash
sudo pip install LumixMaptool
```

use it

```bash
lumixmaptool
```

## Credits
This script is based on [de.rolandkluge.lumix_map_tool](https://github.com/RolandKluge/de.rolandkluge.lumix_map_tool/blob/master/maptool.py) (see also [his article](http://blog.roland-kluge.de/?p=250))

## Packaging

### Python packages

Register the project at PyPI: [LumixMaptool](https://pypi.python.org/pypi/LumixMaptool)

```bash
python setup.py register
```

Update the project:

```bash
python setup.py sdist upload
```

### Debian packages

(Does not work by now)

lumix_map_tool/panasonic-maptool-1.0$ fakeroot dpkg-buildpackage -F

Check results with `lintian`.
