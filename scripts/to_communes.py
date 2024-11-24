import json

def transform_communes_json(input_file, output_file):
    # Read the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get the communes list
    communes = data['communes']
    
    # Sort communes by French name
    communes.sort(key=lambda x: x['name']['fr'].lower())
    
    # Transform the data
    transformed_communes = []
    for i, commune in enumerate(communes, 1):
        # Create new commune object with desired format
        new_commune = {
            "id": f"COM_{str(i).zfill(4)}", # Creates IDs like COM_0001
            "name": {
                "ar": commune['name']['ar'],
                "en": commune['name']['en'],
                "es": commune['name']['es'],
                "fr": commune['name']['fr']
            },
            "region_division_id": commune['region_division_id'],
            "type": commune['type']
        }
        transformed_communes.append(new_commune)
    
    # Create the output dictionary
    output_data = {
        "communes": transformed_communes
    }
    
    # Write to output file with proper indentation and UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

# Example usage
if __name__ == "__main__":
    transform_communes_json('scripts/communes.json', 'transformed_communes.json')
    print("Transformation completed successfully!")