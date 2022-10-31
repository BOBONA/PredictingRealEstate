import time
import datetime
import threading

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from strings import File, Other, Id, Frame
import models
from models import Property, Sale, Feature

with open(File.locators) as file:
    valid_locators = set(file.read().split(" "))
with open(File.bad_locators) as file:
    bad_locators = set(file.read().split(" "))
complete_start = time.time()
global total


def text(browser, id):
    return browser.find_element_by_id(id).text


def populate_database(browser, locators):
    total = 1
    # setup browser
    browser.get(Other.main_url)
    browser.switch_to.frame(Frame.search_input)
    # get references of the locator form
    locator_input = browser.find_element_by_id(Id.locator_input)
    locator_submit = browser.find_element_by_id(Id.locator_submit)
    # get the property for the locator
    for locator in locators:
        if not locator:
            continue
        print(locator + "    " + str((time.time() - complete_start) / total))
        # move browser focus
        browser.switch_to.parent_frame()
        browser.switch_to.frame(Frame.search_input)
        browser.delete_all_cookies()
        # submit locator form
        locator_input.clear()
        locator_input.send_keys(locator)
        locator_submit.click()
        # move browser focus
        browser.switch_to.parent_frame()
        browser.switch_to.frame(Frame.search_results)
        # try to find a better way of finding this element... this is taking too long
        browser.find_element_by_id(
            'tableData'
        ).find_element_by_tag_name(
            'tbody'
        ).find_elements_by_tag_name(
            'tr'
        )[1].find_elements_by_tag_name(
            'td'
        )[2].click()
        browser.switch_to.parent_frame()
        browser.switch_to.frame(Frame.body)
        if Other.unexpected_error in browser.page_source:
            bad_locators.add(locator)
            continue
        # get information from main info page
        address = text(browser, Id.address)
        acres = text(browser, Id.acres)
        land_use_code = text(browser, Id.land_use_code)
        # switch to other info page
        browser.find_element_by_id(Id.more_info).click()
        if Other.no_information in browser.page_source:
            bad_locators.add(locator)
            continue
        # wait until the elements are on the page
        loaded = False
        start = time.time()
        while not loaded:
            try:
                text(browser, Id.units)
            except NoSuchElementException:
                loaded = False
            else:
                loaded = True
            # next locator if it isn't loading quick enough
            if (time.time() - start) > 5:
                break
        if (time.time() - start) > 5:
            continue
        # WebDriverWait(browser, 10).until(
        #     EC.presence_of_element_located((By.ID, 'ctl00_MainContent_DwellingDataRes_labLivingUnits'))
        # )
        remodeled_bath = text(browser, Id.remodeled_bath)
        if remodeled_bath == 'Y':
            remodeled_bath = -1
        recreation_room_area = text(browser, Id.recreation_room_area).split(" ")[0].replace(',', '').strip()
        if recreation_room_area == 'ft2':
            recreation_room_area = ''
        property_fields = {
            'acres': acres.strip(),
            'locator': locator,
            'address': address,
            'units': text(browser, Id.units),
            'year_built': text(browser, Id.year_built),
            'remodeled_year': text(browser, Id.remodeled_year),
            'remodeled_kitchen': text(browser, Id.remodeled_kitchen),
            'remodeled_bath': remodeled_bath,
            'land_use_code': land_use_code,
            'wood_fireplaces': text(browser, Id.fireplaces).split('/')[0].strip(),
            'chimney_stacks': text(browser, Id.fireplaces).split('/')[-1].strip(),
            'metal_fireplaces': text(browser, Id.metal_fireplaces),
            'grade': text(browser, Id.grade),
            'condition': text(browser, Id.condition),
            'style': text(browser, Id.style),
            'living_area': text(browser, Id.living_area).split(" ")[0].replace(',', '').strip(),
            'ground_floor_area': text(browser, Id.ground_floor_area).split(" ")[0].replace(',', '').strip(),
            'recreation_room_area': recreation_room_area,
            'stories': text(browser, Id.stories),
            'rooms': text(browser, Id.rooms),
            'bedrooms': text(browser, Id.bedrooms),
            'bathrooms_full': text(browser, Id.bathrooms).split("/")[0].strip(),
            'bathrooms_half': text(browser, Id.bathrooms).split("/")[-1].strip(),
            'basement_type': text(browser, Id.basement_type),
            'attic_type': text(browser, Id.attic_type),
            'fuel_type': text(browser, Id.fuel_type),
            'heat_type': text(browser, Id.heat_type),
            'heat_system_type': text(browser, Id.heat_system_type),
            'external_wall_type': text(browser, Id.external_wall_type),
            'fixtures': text(browser, Id.fixtures),
        }
        popped = 0
        for key in list(property_fields):
            if not property_fields[key].strip():
                property_fields.pop(key)
                popped += 1
        if popped > 10:
            continue
        sales_fields = []
        if Other.no_sales not in browser.page_source:
            rows = browser.find_element_by_id(
                'divSalesData'
            ).find_element_by_tag_name(
                'tbody'
            ).find_elements_by_tag_name(
                'tr'
            )
            rows.pop(0)
            for row in rows:
                data = row.find_elements_by_tag_name('td')
                date = data[0].text
                price = 0
                if data[1].text:
                    price = data[1].text[1:].replace(',', '').strip()
                type = data[2].text
                sales_fields.append({
                    'date': datetime.datetime.strptime(date, '%m/%d/%Y'),
                    'price': price,
                    'type': type,
                    'validity_code': data[3].text.split('-')[0].strip(),
                    'validity_name': data[3].text.split('-')[1].strip()
                })
        features_fields = []
        features_exist = True
        try:
            browser.find_element_by_id('divObyData')
        except Exception:
            features_exist = False
        if features_exist and Other.no_features not in browser.page_source:
            rows = browser.find_element_by_id('divObyData') \
                .find_element_by_tag_name('tbody') \
                .find_elements_by_tag_name('tr')
            rows.pop(0)
            for row in rows:
                data = row.find_elements_by_tag_name('td')
                year_built = property_fields['year_built']
                if data[1].text:
                    year_built = data[1].text
                units = 1
                if data[2].text:
                    units = data[2].text
                # just converting their formatting to a single number
                area = 0
                if data[3].text:
                    if '=' in data[3].text:
                        area = data[3].text.split('=')[-1].split(' ')[-2].replace(',', '')
                    else:
                        area = data[3].text.replace(',', '')
                grade = ''
                if data[4].text:
                    grade = data[4].text
                condition = ''
                if data[5].text:
                    condition = data[5].text
                features_fields.append({
                    'description': data[0].text,
                    'year_built': year_built,
                    'units': units,
                    'area': area,
                    'grade': grade,
                    'condition': condition
                })
        property = Property.create(**property_fields)
        for sale_fields in sales_fields:
            sale_fields['property'] = property
            Sale.create(**sale_fields)
        for feature_fields in features_fields:
            feature_fields['property'] = property
            Feature.create(**feature_fields)
        total += 1
        with open(File.bad_locators, 'w') as file:
            file.write(" ".join(bad_locators) + " ")


def run(locators, restart=False):
    browser = webdriver.Chrome()
    if restart:
        try:
            populate_database(browser, locators)
        except Exception as e:
            print(e)
            time.sleep(15)
            browser.close()
            run(list(set(locators) - set(list(map(lambda model: model.locator, Property.select())))), restart=True)
    else:
        populate_database(browser, locators)


def run_threads(amount):
    models.initialize()
    for i in range(amount):
        incomplete_locators = list(
            (set(valid_locators) -
             set(list(map(lambda model: model.locator, Property.select())))) -
            set(bad_locators))[::-1]
        thread = threading.Thread(target=run, args=(incomplete_locators[round(i * (len(incomplete_locators) / amount))
                                                                        :round(
            (i + 1) * (len(incomplete_locators) / amount))], True))
        thread.start()


run_threads(3)
