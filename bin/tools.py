# from bcs_modules.common.states import states_abbr
from datetime import datetime
from geopy.distance import distance
from io import StringIO
import uszipcode
import re
import csv
import os


def wrap_double_quotes(text=''):
    return f'"{text}"'


def wrap_single_quotes(text=''):
    return f"'{text}'"


def format_time_stamp(time_format='%m/%d/%Y %H:%M:%S'):
    """ This function returns a timestamp (string) based off of current time """
    try:
        tup = datetime.now().timetuple()
        dm = {tup.index(v): v for v in tup}
        date_map_string = f'{dm[1]}/{dm[2]}/{dm[0]} {dm[3]}:{dm[4]}:{dm[5]}'
        cur_time = datetime.strptime(date_map_string, time_format)
        return cur_time.strftime('%A, %d. %B %Y %H:%M:%S %p')
    except Exception as e:
        print(f'logging error: {e}')
        return ''


def convert_csv_string_to_json(csv_string, limit=0):
    """
    this function converts csv string to json.
    :param csv_string: String
    :param limit: int
    :return: Object
    """
    data_collection = []
    try:
        meta_data = csv_string.split('\n', 1)
        csv_headers = meta_data[0].split(',')
        header_count = len(csv_headers)
        # turn data into file object
        csv_data = csv.reader(StringIO(meta_data[1]), delimiter=',')

        for row in csv_data:
            data_count = len(row)
            # iterate each piece of data and group them by header count
            data_obj = {}
            for index in range(0, header_count):
                # clean up any misc. stuff
                key = format_string_to_clean(csv_headers[index])
                val = format_string_to_clean(row[index])
                if key:
                    data_obj[key] = val
            data_collection.append(data_obj)

        # apply object return limit
        # data_collection = [data_collection[i] for i in range(0, limit)]
        return data_collection

    except Exception as e:
        print(f'Unable to convert string to object.\nError:{e}')
        return [{'message': e}]


def create_name_dict_from_records(records, indexes=None):

    name_dict = {}
    indexes = [0, 1] if (not indexes or type(indexes) is not list) else indexes
    for record in records:
        keys = [*record.keys()]

        if not len(keys):
            # if no keys are somehow found then just continue
            continue

        # cleanup key before hashing
        key = format_string_to_clean(record[keys[indexes[0]]])
        # clean up value before hashing
        value = format_string_to_clean(record[keys[indexes[1]]])
        if key:
            name_dict[key] = value

    return name_dict


def format_string_to_clean(text):
    """
    :param text: text to be "cleansed" of uncanny values (like \n)
    :return: str
    """
    text = re.sub("(\n)", "", text)
    return text


def calculate_distance(src, dst):
    """This function will calculate distance with geo-location coordinates.
        reference for help: https://janakiev.com/blog/gps-points-distance-python/
        mathematical formula: a=hav(Δφ)+cos(φ1)⋅cos(φ2)⋅hav(Δλ)
    """
    geo_coords_distance = -1
    # print(f'source: {src}\n destination: {dst}')
    if ('lat' in src and 'lng' in src) and ('lat' in dst and 'lng' in dst):
        source = (src['lat'], src['lng'])
        destination = (dst['lat'], dst['lng'])
        geo_coords_distance = distance(source, destination).miles

    return geo_coords_distance


class Geolocator:
    """A class that initiates the us-zipcode database and caches zipcode data"""
    def __init__(self):
        self._search = uszipcode.SearchEngine(simple_zipcode=True, db_file_dir="/tmp/")
        self._cache = {}

    def __call__(self, zipcode=''):
        """For the ease of just passing in some zipcode upon object call"""
        try:
            return self._get_cached_data(zipcode)
        except Exception as e:
            print(f'Unable to retrieve cached data.\nError: {e}')

    def _get_cached_data(self, zipcode):
        """Check to see if specific zipcode data exists: small memoizer."""
        if zipcode in self._cache:
            return self._cache[zipcode]

        self._cache[zipcode] = self._retrieve_location_details(zipcode)
        return self._get_cached_data(zipcode)

    def _retrieve_location_details(self, zipcode=''):
        """Simple data retriever by zipcode"""

        location_specs = {}
        if zipcode:
            # print(f'searching for zipcode {zipcode}')
            zipcode_specs = self._search.by_zipcode(str(zipcode)).to_dict()
            if zipcode_specs and zipcode_specs['state'] is not None \
                    and zipcode_specs['lat'] is not None and zipcode_specs['lng'] is not None:
                location_specs = {
                    'state': zipcode_specs['state'],
                    'lat': float(zipcode_specs['lat']),
                    'lng': float(zipcode_specs['lng'])
                }
            else:
                # print(f'Unable to devise location specs with zipcode {zipcode}')
                pass

        return location_specs
