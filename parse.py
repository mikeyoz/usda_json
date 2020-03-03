import csv
import json
from collections import defaultdict

# { fdc_id: { d: description, n: { nutrient_id: amount, ... } }
# d: description
# n: nutrients

print('Processing \'nutrient_spec.csv\'')
with open('data/nutrient_spec.csv') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    assert header[0] == 'id'
    assert header[1] == 'name'
    assert header[2] == 'unit_name'
    nutrients = defaultdict(dict)
    for nutrient in reader:
        nutrients[nutrient[0]]["n"] = nutrient[1]
        nutrients[nutrient[0]]["u"] = nutrient[2]

print('Dumping nutrient data to \'nutrient_spec.json\'')
with open('nutrient_spec.json', 'w') as nutrient_spec:
    json.dump(nutrients, nutrient_spec)

print('Processing \'food_nutrient.csv\'')
with open('data/food_nutrient.csv') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    fdc_id_index = 1
    nutrient_id_index = 2
    amount_index = 3
    assert header[fdc_id_index] == 'fdc_id'
    assert header[nutrient_id_index] == 'nutrient_id'
    assert header[amount_index] == 'amount'
    foods = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for nutrient in reader:
        fdc_id = nutrient[fdc_id_index]
        nutrient_id = nutrient[nutrient_id_index]
        amount = nutrient[amount_index]
        foods[fdc_id]['n'][nutrient_id] = amount

print('Processing \'food.csv\'')
with open('data/food.csv') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    fdc_id_index = 0
    description_index = 2
    assert header[0] == 'fdc_id'
    assert header[2] == 'description'
    for food in reader:
        fdc_id = food[fdc_id_index]
        description = food[description_index]
        if fdc_id in foods:
            foods[fdc_id]['d'] = description

print('Dumping food data to \'usda.json\'')
with open('usda.json', 'w') as usda:
    json.dump(foods, usda)
