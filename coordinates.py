import geopy
import re
import requests
import time

from strings import Other
from models import Property

# geolocator = geopy.Nominatim(user_agent=Other.user_agent)
geolocator = geopy.ArcGIS()
with open("bad_addresses.txt", 'r') as file:
    bad_locators = set(file.read().split(" "))
database_address_pattern = re.compile(r'''
    ^(?P<street_number>\d+)\s
    (?P<street_name>.+)\n
    (?P<county>[\w\s]+),\s?
    (?P<state>\w+)\s?
    (?P<zipcode>\d+)$
''', re.X | re.M)
nomatin_address_pattern = re.compile(r'''
    ^(?P<street_number>\d+),\s?
    (?P<street_name>[\d\s\w]+),\s?
    ([\d\s\w],)?\s?
    (?P<city>\w+),\s?
    (?P<county>[\w\s]+),\s?
    (?P<state>\w+),\s?
    (?P<zipcode>\d+),\s?
    (?P<country>\w+)\s?$
''', re.X)
arcgis_address_pattern = re.compile(r'''
    ^(?P<street_number>\d+)\s?
    (?P<street_name>[\d\s\w]+),\s?
    (?P<city>[\w\s]+),\s?
    (?P<state>\w+),\s?
    (?P<zipcode>\d+)\s?$
''', re.X)


def add_bad_locator(locator):
    with open("bad_addresses.txt", 'a') as file:
        file.write(locator + ' ')


def add_coordinates(property):
    try:
        location = geolocator.geocode(property.address.replace('\n', ''))
    except Exception as e:
        print(e)
    else:
        try:
            latitude = location.latitude
            longitude = location.longitude
            nomatin_address = location.address
        except IndexError:
            add_bad_locator(property.locator)
            return
        else:
            a1 = database_address_pattern.match(property.address)
            if a1 is None:
                add_bad_locator(property.locator)
                return
            else:
                a1 = a1.groupdict()
            matched = arcgis_address_pattern.match(nomatin_address)
            if matched is None:
                add_bad_locator(property.locator)
                return
            a2 = matched.groupdict()
            if a1['zipcode'] != a2['zipcode'] \
                    or a1['street_number'] != a2['street_number'] \
                    or a2['state'] != 'Missouri':
                add_bad_locator(property.locator)
                return
            property.latitude = latitude
            property.longitude = longitude
            property.save(only=[Property.latitude, Property.longitude])


unfinished_properties = Property.select().where(Property.latitude == 0).where(Property.longitude == 0)
for property in unfinished_properties:
    print(property.id)
    if property.locator in bad_locators:
        continue
    time.sleep(0.3)
    add_coordinates(property)
