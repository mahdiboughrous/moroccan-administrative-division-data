import json

def update_and_sort_data(regions_file, divisions_file, communes_file, output_dir):
    # Load regions.json
    with open(regions_file, 'r', encoding='utf-8') as f:
        regions_data = json.load(f)

    # Load region-divisions.json
    with open(divisions_file, 'r', encoding='utf-8') as f:
        divisions_data = json.load(f)

    # Load communes.json
    with open(communes_file, 'r', encoding='utf-8') as f:
        communes_data = json.load(f)

    # Step 1: Sort regions alphabetically by name.en
    regions_data['regions'].sort(key=lambda x: x['name']['en'])
    region_id_map = {}

    # Assign new region IDs
    for i, region in enumerate(regions_data['regions'], start=1):
        new_region_id = f"REGION_{i:02}"
        region_id_map[region['id']] = new_region_id
        region['id'] = new_region_id

    # Step 2: Update and sort divisions
    for division in divisions_data['region_divisions']:
        division['region_id'] = region_id_map[division['region_id']]  # Update region_id in divisions
    divisions_data['region_divisions'].sort(key=lambda x: x['name']['en'])

    division_id_map = {}
    for i, division in enumerate(divisions_data['region_divisions'], start=1):
        new_division_id = f"DIV_{i:03}"
        division_id_map[division['id']] = new_division_id
        division['id'] = new_division_id

    # Step 3: Update and sort communes
    for commune in communes_data['communes']:
        commune['region_division_id'] = division_id_map[commune['region_division_id']]  # Update region_division_id
    communes_data['communes'].sort(key=lambda x: x['name']['en'])

    commune_id_map = {}
    for i, commune in enumerate(communes_data['communes'], start=1):
        new_commune_id = f"COM_{i:04}"
        commune_id_map[commune['id']] = new_commune_id
        commune['id'] = new_commune_id

    # Step 4: Save the updated files
    with open(f"{output_dir}/regions.json", 'w', encoding='utf-8') as f:
        json.dump(regions_data, f, ensure_ascii=False, indent=4)

    with open(f"{output_dir}/region-divisions.json", 'w', encoding='utf-8') as f:
        json.dump(divisions_data, f, ensure_ascii=False, indent=4)

    with open(f"{output_dir}/communes.json", 'w', encoding='utf-8') as f:
        json.dump(communes_data, f, ensure_ascii=False, indent=4)

# File paths
input_regions_file = './data/regions.json'
input_divisions_file = './data/region-divisions.json'
input_communes_file = './data/communes.json'
output_directory = './data'

# Update and sort data
update_and_sort_data(input_regions_file, input_divisions_file, input_communes_file, output_directory)
