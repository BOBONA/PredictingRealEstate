from peewee import *

from strings import File

DATABASE = SqliteDatabase(File.database)


# More information: http://revenue.stlouisco.com/ias/Glossary.aspx#Property
class Property(Model):
    # An id used by St. louis county
    locator = TextField(unique=True)
    latitude = DoubleField(default=0)
    longitude = DoubleField(default=0)
    # The address is in the form of "street_number street street_suffix
    #                                city, state_abbreviation zip_code"
    address = TextField()
    # A code that describes the use of the property
    # Codes: http://revenue.stlouisco.com/ias/LandUseCodes.htm
    land_use_code = IntegerField()
    acres = FloatField(default=0)
    # The year the house was last remodeled
    remodeled_year = IntegerField(default=0)
    # The number of remodeled_kitchens
    # Doesn't seem reliable
    remodeled_kitchen = IntegerField(default=0)
    # The number of remodeled_baths
    # Sometimes, instead of a number, there would be the letter Y. I set those to -1
    # Doesn't seem reliable
    remodeled_bath = IntegerField(default=0)
    wood_fireplaces = IntegerField(default=0)
    chimney_stacks = IntegerField(default=0)
    metal_fireplaces = IntegerField(default=0)
    # The number of plumbing fixtures
    fixtures = IntegerField(default=0)
    # The number of living units
    units = IntegerField(default=0)
    year_built = IntegerField(default=0)
    # The grade is the base construction quality based upon certain construction specifications and the quality of
    # materials and workmanship. From high to low: X+-, A+-, B+-, C+-, D+-, E+-. There is also an S grade that the
    # website didn't mention. S is less common that X, so either they changed their system, some of their workers
    # thought that S was the highest instead of X, or S is higher than X.
    grade = TextField(default='')
    # Options:
    # EX - EXCELLENT, VG - VERY GOOD, GD - GOOD, AV - AVERAGE, FR - FAIR, PR - POOR, VP - VERY POOR, UN - UNSOUND
    condition = TextField(default='')
    # Options: 13 (could be condo), 14, 15, 16, 17, RANCH, CONVENTIONAL, BUNGALOW, PLAN URBAN DEVELOPMENT, COLONIAL,
    # OLD STYLE, CAPE COD, SPLIT FOYER, SPLIT LEVEL, CONTEMPORARY, CONDOMINIUM, OTHER
    style = TextField(default='')
    # Living area in square feet
    living_area = IntegerField(default=0)
    # Complete floor area in square feet
    ground_floor_area = IntegerField(default=0)
    # Recreation room area in square feet
    recreation_room_area = IntegerField(default=0)
    # Number of floors
    stories = FloatField(default=0)
    # Excluding rooms in basement
    rooms = IntegerField(default=0)
    bedrooms = IntegerField(default=0)
    bathrooms_full = IntegerField(default=0)
    bathrooms_half = IntegerField(default=0)
    # Options: FULL, NONE, PART, CRAWL
    basement_type = TextField(default='')
    # Options: NONE, FULL FINISHED, FULL FINISHED WITH WALL HEIGHT, PART FINISHED, UNFINISHED
    attic_type = TextField(default='')
    # Options: GAS, ELECTRIC, OIL, WOOD, NONE, SOLAR
    fuel_type = TextField(default='')
    # The type of heat being used
    # Options: WARM AIR, RADIANT, HOT WATER, ELECTRIC, NONE
    heat_type = TextField(default='')
    # The type of heat system
    # Options: CENTRAL WITH AC, BASIC, NONE
    heat_system_type = TextField(default='')
    # Options: BRICK, ALUMINUM / VINYL, MASONRY AND FRAME, ASBESTOS, STUCCO, FRAME, STONE, BLOCK, CONCRETE
    external_wall_type = TextField(default='')

    class Meta:
        database = DATABASE
        db_table = 'Property'

    @classmethod
    def get_valid_properties(cls):
        return cls.select().where(
            Property.land_use_code == 110
        ).where(
            Property.units == 1
        ).where(
            Property.longitude != 0
        ).where(
            Property.latitude != 0
        )

    def get_proper_sales(self):
        return Sale.select().where(
            Sale.property == self
        ).where(
            Sale.price > 1000
        ).where(
            Sale.validity_code == 'X'
        )


class Sale(Model):
    date = DateField()
    price = IntegerField()
    property = ForeignKeyField(Property, related_name='sales')
    # Options: LAND AND BUILDING, LAND ONLY, BUILDING ONLY
    type = TextField(default='')
    # These can be many things, just filter all the sales that have validity_code as X
    # or/and validity_name as VALID SALE
    validity_code = TextField(default='')
    validity_name = TextField(default='')

    class Meta:
        database = DATABASE
        db_table = 'Sale'


class Feature(Model):
    property = ForeignKeyField(Property, related_name='features')
    # Go to features.txt for a list of these
    description = TextField(default='')
    year_built = IntegerField(default=0)
    # The amount of the feature
    units = IntegerField(default=0)
    # The area in square feet
    area = IntegerField(default=0)
    # A grade of the feature that can be A, B, C, D, E
    grade = TextField(default='')
    # Options: EXCELLENT, GOOD, NORMAL, AVERAGE, FAIR, POOR, UNSOUND
    condition = TextField(default='')

    class Meta:
        database = DATABASE
        db_table = 'Feature'


def initialize():
    DATABASE.close()
    DATABASE.connect()
    DATABASE.create_tables([Property, Sale, Feature], safe=True)
    DATABASE.close()
