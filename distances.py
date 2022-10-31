from math import radians, asin, sin, sqrt, cos

import time
import h5py
import numpy

from models import Property

models = list(Property.select())
print("Models loaded")
file_name = 'distances.h5'
highest_distance = 100000


def haversine(lon1, lat1, lon2, lat2):
    # decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # radius of earth in kilometers
    return c * r


def calculate_properties_within_distance(index, current_range):
    # update the file if the distance has never been calculated
    file = h5py.File(file_name, 'a')
    if str(current_range * 10000) not in file:
        group = file.create_group(str(current_range * 10000))
        group.create_dataset('indexes', (0,),
                             dtype=h5py.special_dtype(vlen=numpy.dtype('uint32')),
                             maxshape=(None,), compression='gzip')
        group.create_dataset('distances', (0,),
                             dtype=h5py.special_dtype(vlen=numpy.dtype('float16')),
                             maxshape=(None,), compression='gzip')
        group.create_dataset('last_updated', (0,), maxshape=(None,), compression='gzip')
    # resize the arrays to the right length
    indexes = file.get(str(current_range * 10000)).get('indexes')
    distances = file.get(str(current_range * 10000)).get('distances')
    last_updated = file.get(str(current_range * 10000)).get('last_updated')
    indexes.resize((max(len(indexes), index + 1),))
    distances.resize((max(len(distances), index + 1),))
    last_updated.resize((max(len(last_updated), index + 1),))
    # find the closest pre calculated range
    closest_range = highest_distance
    in_range = []
    last_model_size = 0
    # the indexes to be calculated are going to be a mix of the ones definitely in range from the closest range that
    # has already been calculated + a range of the differences between model sizes. Using this i can find the optimal
    # closest_range to use.
    for group in file:
        try:
            in_range1 = list(file.get(group).get('indexes')[index])
            last_model_size1 = int(file.get(group).get('last_updated')[index])
        except ValueError:
            continue
        if (len(in_range1) + (len(models) - last_model_size1) <
                len(in_range) + (len(models) - last_model_size)):
            closest_range = float(group)
            in_range = in_range1
            last_model_size = last_model_size1
        # r = float(group)
        # if closest_range > r >= current_range:
        #     closest_range = r
        #     in_range = list(file.get(group).get('indexes')[index])
        #     last_model_size = int(file.get(group).get('last_updated')[index])
    # exit if we have already calculated the indexes for 'distance' and the model size hasn't changed
    if closest_range == current_range and file.get(str(current_range * 10000)).get('last_updated')[index] == len(models):
        return
    # first iterate over the indexes that are valid for the closest_range and see if they match the current range. if
    # we have already calculated for the current_range just with a different model size, then there is no need to
    # recalculate most of it
    if closest_range == current_range and len(in_range) > 0:
        valid_indexes = in_range[:]
        valid_distances = file.get(str(current_range * 10000)).get('distances')[index]
        to_calculate = list(range(last_model_size, len(models)))
    else:
        valid_indexes = []
        valid_distances = []
        to_calculate = in_range + list(range(last_model_size, len(models)))
    for i in to_calculate:
        model = models[index]
        other = models[i]
        distance = haversine(model.longitude, model.latitude, other.longitude, other.latitude)
        if distance <= current_range:
            valid_indexes.append(i)
            valid_distances.append(distance)
    indexes[index] = valid_indexes
    distances[index] = valid_distances
    last_updated[index] = len(models)
    file.close()


for i in range(0, len(models)):
    calculate_properties_within_distance(i, 0.3)
    print(i)
