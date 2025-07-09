import pandas as pd
from textpro import entity_unit_map
import re
import csv


csv_file_path = 'Img_text_new.csv'

df = pd.read_csv(csv_file_path)
test_file = pd.read_csv('Resource\\1000_data.csv')

text_list = df['text']
entity_values = test_file['entity_name']


flattened_entity_unit_map = {
    entity: {unit: measurement 
            for measurement, units in measurements.items() 
            for unit in units}
    for entity, measurements in entity_unit_map.items()
}

def find_units1(text, entity):
    if entity not in flattened_entity_unit_map:
        return []

    allowed_units = flattened_entity_unit_map[entity]
    pattern = r'(\d+(\.\d+)?)\s*(' + '|'.join(re.escape(unit) for unit in allowed_units) + r')\b'
    
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    result = []
    for match in matches:
        number = match[0]
        unit = match[2]
        full_unit_name = next(measurement for measurement, units in entity_unit_map[entity].items() if unit.lower() in [u.lower() for u in units])
        result.append((number, full_unit_name))
    
    return result

# Open the CSV file once, outside the loop
with open('units_found.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Image_id", "Units", "Entity_value"])

    for i, (text, entity) in enumerate(zip(text_list, entity_values)):
        if isinstance(text, str):
            units_f = find_units1(text, entity)
            if units_f:
                for number, unit in units_f:
                    writer.writerow([i, f"{number} {unit}", entity])
            else:
                writer.writerow([i, "----", entity])

print("CSV created")