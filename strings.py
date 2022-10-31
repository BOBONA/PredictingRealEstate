class Frame:
    search_input = 'SearchInput'
    search_results = 'SearchResults'
    body = 'body'


class Other:
    main_url = 'http://revenue.stlouisco.com/ias/'
    unexpected_error = 'An unexpected issue has occurred while showing'
    no_information = 'Dwelling/Building and Yard Improvement Information Not Found'
    no_sales = 'There is no sales information available for this parcel.'
    no_features = 'There is no other building and yard information available for this parcel and tax year.'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    email = 'jameshagua@gmail.com'


class Id:
    locator_input = 'tboxLocatorNum'
    locator_submit = 'butFind'
    address = 'ctl00_MainContent_OwnLeg_labTaxAddr'
    acres = 'ctl00_MainContent_OwnLeg_labAcres'
    land_use_code = 'ctl00_MainContent_OwnLeg_labLandUseCode'
    more_info = 'ctl00_LeftMargin_MarginLinks_divPropLink'
    units = 'ctl00_MainContent_DwellingDataRes_labLivingUnits'
    year_built = 'ctl00_MainContent_DwellingDataRes_labYearBuilt'
    remodeled_year = 'ctl00_MainContent_DwellingDataRes_labRemodYear'
    remodeled_kitchen = 'ctl00_MainContent_DwellingDataRes_labRemodKit'
    remodeled_bath = 'ctl00_MainContent_DwellingDataRes_labRemBath'
    fireplaces = 'ctl00_MainContent_DwellingDataRes_labWoodFirePl'
    metal_fireplaces = 'ctl00_MainContent_DwellingDataRes_labMetalFirePl'
    grade = 'ctl00_MainContent_DwellingDataRes_labGrade'
    condition = 'ctl00_MainContent_DwellingDataRes_labCDU'
    style = 'ctl00_MainContent_DwellingDataRes_labStyle'
    living_area = 'ctl00_MainContent_DwellingDataRes_labTotLivingArea'
    ground_floor_area = 'ctl00_MainContent_DwellingDataRes_labMGFA'
    recreation_room_area = 'ctl00_MainContent_DwellingDataRes_labRecRmArea'
    stories = 'ctl00_MainContent_DwellingDataRes_labNumStories'
    rooms = 'ctl00_MainContent_DwellingDataRes_labTotRooms'
    bedrooms = 'ctl00_MainContent_DwellingDataRes_labTotBedRooms'
    bathrooms = 'ctl00_MainContent_DwellingDataRes_labTotBaths'
    basement_type = 'ctl00_MainContent_DwellingDataRes_labBasement'
    attic_type = 'ctl00_MainContent_DwellingDataRes_labAttic'
    fuel_type = 'ctl00_MainContent_DwellingDataRes_labFuelType'
    heat_type = 'ctl00_MainContent_DwellingDataRes_labHeatSys'
    heat_system_type = 'ctl00_MainContent_DwellingDataRes_labHeat'
    external_wall_type = 'ctl00_MainContent_DwellingDataRes_labExtWall'
    fixtures = 'ctl00_MainContent_DwellingDataRes_labTotFixtures'


class File:
    database = 'properties.db'
    locators = 'locators.txt'
    bad_locators = 'bad_locators.txt'


class NumericStringValues:
    grades = {
        "": 0, "E-": 0, "E": 1, "E+": 2, "D-": 3, "D": 4, "D+": 5, "C-": 6, "C": 7, "C+": 8, "B-": 9, "B": 10, "B+": 11,
        "A-": 12, "A": 13, "A+": 14, "S-": 15, "S": 16, "S+": 17, "X-": 18, "X": 19, "X+": 20
    }
    conditions = {
        "": 0,
        "UN - UNSOUND": 0,
        "VP - VERY POOR": 1,
        "PR - POOR": 2,
        "FR - FAIR": 3,
        "AV - AVERAGE": 4,
        "GD - GOOD": 5,
        "VG - VERY GOOD": 6,
        "EX - EXCELLENT": 7
    }


class NonNumericStringValues:
    pass
