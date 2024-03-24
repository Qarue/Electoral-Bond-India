import json

def load_json_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def combine_bonds(buyers_data, consumers_data):

    sum = 0
    for consumer in consumers_data:
        sum = sum + consumer["Denominations"]


    return sum

# Load data
buyers_data = load_json_data('buyers_data.json')
consumers_data = load_json_data('consumers_data.json')

# Combine and generate the new dataset
combined_data = combine_bonds(buyers_data, consumers_data)


print(combined_data)
