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
"""

from argparse import ArgumentParser, RawTextHelpFormatter, Action
import os
import re
from pyparsing import Word, alphas, nums, OneOrMore, alphanums
import shutil
import logging

logfile = os.path.join(os.path.expanduser("~"), 'maptool.log')
logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s %(message)s')

__version__ = "1.0.8"

region_mapping = {}
region_mapping[1] = 'Japan'
region_mapping[2] = 'South Asia, Southeast Asia'
region_mapping[3] = 'Oceania'
region_mapping[4] = 'North America, Central America'
region_mapping[5] = 'South America'
region_mapping[6] = 'Northern Europe'
region_mapping[7] = 'Eastern Europe'
region_mapping[8] = 'Western Europe'
region_mapping[9] = 'West Asia, Africa'
region_mapping[10] = 'Russia, North Asia'

def is_valid_mapdata(parser, path_to_mapdata):
    """Check if path_to_mapdata is a valid path."""
    if os.path.isfile(path_to_mapdata):
        return path_to_mapdata
    else:
        if path_to_mapdata == '':
            parser.error("You have to specify the path to the mapdata file (it's on a DVD).")
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
    with open(path_to_mapdata, 'r') as f:
        mapdata = f.read()
    mapdata_pattern = re.compile("\s*(\d{8})\s*(\d{8})\s*(.*)\s*", re.DOTALL)
    num1, num2, data = mapdata_pattern.findall(mapdata)[0]

    parsed_map_data = {'num1': num1, 'num2': num2, 'regions': {}}
    def regionParsing(x):
        parsed_map_data['regions'][int(x[0])] = x[1:]

    regionnum = Word(nums, exact=2).setResultsName("region-number").setName("region-number")
    filename = Word(alphanums + "/.").setResultsName("filename").setName("filename")
    regiondata = Word("{").suppress() + OneOrMore(filename) + Word("}").suppress()
    regiondata = regiondata.setResultsName("region-data").setName("region-data")
    region = (regionnum + regiondata).setResultsName("region").setName("region")
    region.setParseAction(regionParsing)
    map_grammar = OneOrMore(region)

    data = data.strip() # a strange character at the end
    map_grammar.parseString(data)

    return parsed_map_data

def copy_maps(path_to_mapdata, path_to_sdcard, regions):
    """Copy map information of regions to sdcard."""
    mapdata_cd_folder = '/'.join(path_to_mapdata.split("/")[:-1])
    logging.info("mapdata_cd_folder: %s" % mapdata_cd_folder)
    #mapdata_on_sdcard = path_to_sdcard + "/PRIVATE/MAP_DATA"
    
    # This works with Panasonic Lumix DMC TZ-41
    mapdata_on_sdcard = os.path.join(path_to_sdcard, "PRIVATE/PANA_GRP/PAVC/LUMIX/MAP_DATA")
    if not os.path.exists(mapdata_on_sdcard):
        os.makedirs(mapdata_on_sdcard)
    mapdata = parse_mapdata(path_to_mapdata)

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

            logging.info("abspath_to_source_file: %s" % abspath_to_source_file)
            logging.info("target_dir: %s" % target_dir)
            logging.info("target_file: %s" % target_file)

            if not os.path.exists(target_dir):
                os.mkdir(target_dir)

            if not os.path.exists(target_file):
                shutil.copy(abspath_to_source_file, target_dir)
        print("Copying region '%i' DONE" % selected_region_id)
    print("All operations exited succesfully.")

class UniqueAppendAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        unique_values = set(values)
        setattr(namespace, self.dest, unique_values)

def autodetect_mapdata():
    """Try to find the DVD with map data."""
    path = "/media"
    subdir = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    while len(subdir) == 1:
        path = os.path.join(path, subdir[0])
        subdir = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    if "MAP_DATA" in subdir:
        path = path = os.path.join(path, "MAP_DATA/MapList.dat")
        return path
    return ""

def main():
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)

    # Add more options if you like
    parser.add_argument("-m", "--mapdata", dest="mapdata", metavar="MAPDATA",
                    default=autodetect_mapdata(),
                    help="path to MAPDATA folder on the Lumix DVD",
                    type=lambda x: is_valid_mapdata(parser, x))
    parser.add_argument("-s", "--sdcard", dest="path_to_sdcard", metavar="SDCARD",
                    required=True,
                    help="path to SDCARD",
                    type=lambda x: is_valid_sdcard(parser, x))
    parser.add_argument("-r", "--regions", dest="regions", nargs='+', 
                    required=True, choices=list(range(1,11)), type=int,
                    action=UniqueAppendAction,
                    help="The space-separated indices of the regions to copy. " \
                    + "E.g. 1 6 10. At least one region needs to be given. " \
                    + "Regions are:\n" \
                    + "\n".join(list(map(lambda i: "%i -\t%s" % (i, region_mapping[i]), range(1,11)))))
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()
    copy_maps(args.mapdata, args.path_to_sdcard, args.regions)

if __name__ == "__main__":
    main()