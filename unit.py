import pandas as pd
import re
import csv

# Read the input CSV files
csv_file_path = 'Img_text_new.csv'
df = pd.read_csv(csv_file_path)
test_file = pd.read_csv('Resource\\1000_data.csv')

# Extract text and entity values
text_list = df['text']
entity_values = test_file['entity_name']

# Define entity_unit_map (as provided in your code)
entity_unit_map = {
    'width': {
        'centimetre': ['cm','c.m.', 'cm.', 'centimeter','centimetre','cms','centimeters'],
        'foot':['ft','feet','foot','\''], 
        'inch':['inches','in','\"','inch'], 
        'metre':['metre','meters','m','m.'],
        'millimetre':['millimetre','mm','mm.','m.m.','mmtr','millimet.'], 
        'yard':[ "yd", "yd.", "yards","yrd","yrds","y.", "y.d.","yds","y.d","y.", "yds.",  "yrd.","yrds.", "yrd","yds." ]        
    },
    'depth': {
        'centimetre': ['cm','c.m.', 'cm.', 'centimeter','centimetre','cms','centimeters'],
        'foot':['ft','feet','foot','\''], 
        'inch':['inches','in.','\"','inch'], 
        'metre':['metre','meters','m','m.'],
        'millimetre':['millimetre','mm','mm.','m.m.','mmtr','millimet.'], 
        'yard':[ "yd", "yd.", "yards","yrd","yrds","y.", "y.d.","yds","y.d","y.", "yds.",  "yrd.","yrds.", "yrd","yds." ]        
    },
    'height': {
        'centimetre': ['cm','c.m.', 'cm.', 'centimeter','centimetre','cms','centimeters'],
        'foot':['ft','feet','foot','\''], 
        'inch':['inches','in.','\"','inch'], 
        'metre':['metre','meters','m','m.'],
        'millimetre':['millimetre','mm','mm.','m.m.','mmtr','millimet.'], 
        'yard':[ "yd", "yd.", "yards","yrd","yrds","y.", "y.d.","yds","y.d","y.", "yds.",  "yrd.","yrds.", "yrd","yds." ]        
    },
}

# Flatten the entity_unit_map
flattened_entity_unit_map = {
    entity: {unit.lower(): measurement 
            for measurement, units in measurements.items() 
            for unit in units}
    for entity, measurements in entity_unit_map.items()
}

csv_file_path = 'Img_text_new.csv'
df = pd.read_csv(csv_file_path)
test_file = pd.read_csv('Resource\\1000_data.csv')

text_list = df['text']
entity_values = test_file['entity_name']
image_ids = df['img_id']  # Assuming there's an 'img_id' column in your CSV

# Keep the entity_unit_map and flattened_entity_unit_map as they are

def find_units1(text, entity):
    if entity not in flattened_entity_unit_map:
        return None

    allowed_units = flattened_entity_unit_map[entity]
    pattern = r'(\d+(\.\d+)?)\s*(' + '|'.join(re.escape(unit) for unit in allowed_units) + r')\b'
    
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    if matches:
        number, _, unit = matches[0]
        measurement = allowed_units[unit.lower()]
        return f"{number} {unit}"
    
    return None

# Write to CSV
with open('units_found.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Image_id", "Units"])

    for i, (text, entity, img_id) in enumerate(zip(text_list, entity_values, image_ids)):
        if isinstance(text, str):
            unit_found = find_units1(text, entity)
            if unit_found:
                writer.writerow([img_id, unit_found])
            else:
                writer.writerow([img_id, "----"])

print("CSV created")