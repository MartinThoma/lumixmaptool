#!/usr/bin/env python

"""
Author: Martin Thoma <info@martin-thoma.de>,
        based on https://github.com/RolandKluge/de.rolandkluge.lumix_map_tool/
        from Roland Kluge.

Manage GPS information for Panasonic Lumix cameras.

Panasonic offers GPS metadata to add to a SD card. This metadata can contain
tourist information that might be useful for sightseeing. This maptool helps
to copy the data from Lumix DVD to the SD card that is inserted into your
computer (the camera has not to be connected).
This script was tested with Lumix TZ41.
"""

import os
import sys
import re
import shutil
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Action
from pyparsing import Word, nums, OneOrMore, alphanums

logfile = os.path.join(os.path.expanduser("~"), 'maptool.log')

__version__ = "1.0.13"

region_mapping = {
    1: 'Japan',
    2: 'South Asia, Southeast Asia',
    3: 'Oceania',
    4: 'North America, Central America',
    5: 'South America',
    6: 'Northern Europe',
    7: 'Eastern Europe',
    8: 'Western Europe',
    9: 'West Asia, Africa',
    10: 'Russia, North Asia'
}


def is_valid_mapdata(parser, path_to_mapdata):
    """Check if path_to_mapdata is a valid path."""
    if os.path.isfile(path_to_mapdata):
        return path_to_mapdata
    else:
        if path_to_mapdata == '':
            parser.error("You have to specify the path to the mapdata file "
                         + "(it's on a DVD).")
        else:
            parser.error("The file '%s' does not exist." % path_to_mapdata)


def is_valid_sdcard(parser, path_to_sdcard):
    """Check if sdcard is a valid path."""
    if not os.path.exists(path_to_sdcard):
        parser.error("The path '%s' does not exist." % path_to_sdcard)
    if not os.access(path_to_sdcard, os.W_OK):
        parser.error("The path '%s' is not writable" % path_to_sdcard)
    else:
        return path_to_sdcard


def parse_mapdata(path_to_mapdata):
    """Parse mapdata file into a dictionary that has three values:
        num1 (a magic number), num2 (a magic number) and regions which
        itself is a dictionary that contains region numbers as keys and
        the files as a list.
    """
    with open(path_to_mapdata, 'r') as f:
        mapdata = f.read()
    mapdata_pattern = re.compile("(\d{8})\s*(\d{8})\s*(.*)", re.DOTALL)
    num1, num2, data = mapdata_pattern.findall(mapdata)[0]
    match = re.search(mapdata_pattern, mapdata)
    if not match:
        print("An error occured.")
        print("The file '%s' was not well-formed." % path_to_mapdata)
        sys.exit()
    num1, num2, data = match.groups()
    logging.debug("num1: %s" % num1)
    logging.debug("num2: %s" % num2)
    logging.debug("data: %s" % data)

    parsed_map_data = {'num1': num1, 'num2': num2, 'regions': {}}

    def regionParsing(x):
        parsed_map_data['regions'][int(x[0])] = x[1:]

    def named(name, rule):
        return rule.setResultsName(name).setName(name)

    regionnum = named("region-number", Word(nums, exact=2))
    filename = named("filename", Word(alphanums + "/."))
    tmp = Word("{").suppress() + OneOrMore(filename) + Word("}").suppress()
    regiondata = named("region-data", tmp)
    region = named("region", (regionnum + regiondata))

    region.setParseAction(regionParsing)
    map_grammar = OneOrMore(region)

    data = data.strip()  # a strange character at the end
    map_grammar.parseString(data)

    return parsed_map_data


def copy_maps(path_to_mapdata, path_to_sdcard, regions):
    """Copy map information of regions to sdcard."""
    mapdata_cd_folder = '/'.join(path_to_mapdata.split("/")[:-1])
    logging.info("mapdata_cd_folder: %s" % mapdata_cd_folder)
    #mapdata_on_sdcard = path_to_sdcard + "/PRIVATE/MAP_DATA"

    # This works with Panasonic Lumix DMC TZ-41
    mapdata_on_sdcard = os.path.join(path_to_sdcard,
                                     "PRIVATE/PANA_GRP/PAVC/LUMIX/MAP_DATA")
    logging.info("mapdata_on_sdcard: %s" % mapdata_on_sdcard)
    if not os.path.exists(mapdata_on_sdcard):
        os.makedirs(mapdata_on_sdcard)
    mapdata = parse_mapdata(path_to_mapdata)
    logging.info("mapdata: %s" % mapdata)

    # Delete previously stored cards
    shutil.rmtree(mapdata_on_sdcard, ignore_errors=True)

    # And create the directory again
    os.makedirs(mapdata_on_sdcard)

    for selected_region_id in regions:
        print("Copying region '%s' ..." % selected_region_id)
        for path in mapdata['regions'][selected_region_id]:
            logging.info("Copy file %s" % path)
            subdir, filename = path.split("/")
            abspath_to_source_file = os.path.join(mapdata_cd_folder, path)
            target_dir = mapdata_on_sdcard + "/" + subdir
            target_file = target_dir + "/" + filename

            logging.debug("abspath_to_source_file: %s" % abspath_to_source_file)
            logging.debug("target_dir: %s" % target_dir)
            logging.debug("target_file: %s" % target_file)

            if not os.path.exists(target_dir):
                os.mkdir(target_dir)

            if not os.path.exists(target_file):
                os.system("cp %s %s" % (abspath_to_source_file, target_dir))
        print("Copying region '%i' DONE" % selected_region_id)
    print("All operations exited succesfully.")


class UniqueAppendAction(Action):
    """Make sure that the list of regions contains unique values."""
    def __call__(self, parser, namespace, values, option_string=None):
        unique_values = set(values)
        setattr(namespace, self.dest, unique_values)


def autodetect_mapdata():
    """Try to find the DVD with map data."""
    path = "/media"
    subdir = [f for f in os.listdir(path)
              if os.path.isdir(os.path.join(path, f))]
    while len(subdir) == 1:
        path = os.path.join(path, subdir[0])
        subdir = [f for f in os.listdir(path)
                  if os.path.isdir(os.path.join(path, f))]

    if "MAP_DATA" in subdir:
        path = path = os.path.join(path, "MAP_DATA/MapList.dat")
        return path
    return ""


def main(mapdata, path_to_sdcard, regions):
    copy_maps(mapdata, path_to_sdcard, regions)


def get_parser():
    """Return the parser object for this script."""
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)

    # Add more options if you like
    parser.add_argument("-m", "--mapdata",
                        dest="mapdata",
                        metavar="MAPDATA",
                        default=autodetect_mapdata(),
                        help=("path to MAPDATA/MapList.dat file "
                              "on the Lumix DVD"),
                        type=lambda x: is_valid_mapdata(parser, x))
    parser.add_argument("-s", "--sdcard",
                        dest="path_to_sdcard",
                        metavar="SDCARD",
                        required=True,
                        help="path to SDCARD",
                        type=lambda x: is_valid_sdcard(parser, x))

    helptext = "The space-separated indices of the regions to copy. "
    helptext += "E.g. 1 6 10. At least one region needs to be given. "
    helptext += "Regions are:\n"
    tmp = map(lambda i: "%i -\t%s" % (i, region_mapping[i]),
              region_mapping.keys())
    helptext += "\n".join(list(tmp))
    parser.add_argument("-r", "--regions",
                        dest="regions",
                        nargs='+',
                        required=True,
                        choices=list(range(1, 11)),
                        type=int,
                        action=UniqueAppendAction,
                        help=helptext)
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__)
    return parser

if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.mapdata, args.path_to_sdcard, args.regions)
