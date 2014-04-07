LumixMaptool
==============

System independant map managment tool for Lumix Digital Cameras (especially Lumix TZ41).

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
