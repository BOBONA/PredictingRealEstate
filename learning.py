import h5py
from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor

from strings import NumericStringValues
from models import Property


MODEL_COUNT = 20
MAX_DEPTH = 10
MAX_DISTANCE = 0.5
MAX_TIME_DIFFERENCE = 2
WEIGHT_A = 1.4
WEIGHT_B = 3
WEIGHT_C = 5

# TODO if I change Property.select() to Property.getValidProperties(), I need to recalculate distances
models = list(Property.select())
print('models loaded!')

file = h5py.File('distances.h5', 'r')
data = file.get('5000.0')
indexes = data.get('indexes')
distances = data.get('distances')


def weight(distance, time_difference):
    return WEIGHT_A ** (-WEIGHT_B * distance - WEIGHT_C * time_difference)


def price_per_foot(model_index, year):
    sales = []
    for i in range(len(indexes[model_index])):
        other = models[indexes[model_index][i]]
        distance = distances[model_index][i]
        if distance > MAX_DISTANCE:
            continue
        for sale in other.get_proper_sales():
            if sale.date.year >= year:
                continue
            time_difference = year - sale.date.year
            if time_difference > MAX_TIME_DIFFERENCE:
                continue
            sales.append((sale, distance, time_difference))
    if sales:
        total_weight = sum([
            weight(distance, time_difference)
            for (sale, distance, time_difference) in sales
        ])
        if total_weight:
            return sum([
                (weight(distance, time_difference) / total_weight) * (sale.price / sale.property.living_area)
                for (sale, distance, time_difference) in sales
            ])


def learn():
    tree = DecisionTreeRegressor(MAX_DEPTH)
    sales = []
    prices = []
    test_sales = []
    test_prices = []
    for index, model in enumerate(models[0:MODEL_COUNT]):
        print(str(index))
        for i, sale in enumerate(model.get_proper_sales()):
            per_foot = price_per_foot(index, sale.date.year)
            if per_foot is None:
                continue
            features = [
                per_foot,
                sale.date.year,
                model.acres,
                (model.remodeled_year - model.year_built) if (model.remodeled_year - model.year_built) > 0
                else model.year_built,
                model.wood_fireplaces,
                model.metal_fireplaces,
                model.chimney_stacks,
                model.fixtures,
                (sale.date.year - model.year_built),
                NumericStringValues.grades[model.grade],
                NumericStringValues.conditions[model.condition],
                model.living_area,
                model.ground_floor_area,
                model.recreation_room_area,
                model.stories,
                model.rooms,
                model.bedrooms,
                model.bathrooms_full,
                model.bathrooms_half,
            ]
            if len(sales) == 1 or index != 0:
                sales.append(features)
                prices.append(sale.price)
            else:
                test_sales.append(features)
                test_prices.append(sale.price)
    tree.fit(sales, prices)
    prediction = tree.predict(test_sales)
    error = mean_absolute_error(test_prices, prediction)
    return error


print(learn())
