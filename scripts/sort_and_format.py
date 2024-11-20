import json
import os

def sort_and_update_ids(regions_file, divisions_file, output_regions_file, output_divisions_file):
    # Load regions.json
    with open(regions_file, 'r', encoding='utf-8') as f:
        regions_data = json.load(f)
    
    # Load region-divisions.json
    with open(divisions_file, 'r', encoding='utf-8') as f:
        divisions_data = json.load(f)
    
    # Step 1: Sort regions alphabetically by `name.en`
    sorted_regions = sorted(regions_data['regions'], key=lambda x: x['name']['en'])
    
    # Step 2: Update region IDs based on new order
    region_id_map = {}
    for i, region in enumerate(sorted_regions, start=1):
        new_id = f"REGION_{str(i).zfill(2)}"
        region_id_map[region['id']] = new_id
        region['id'] = new_id  # Update region ID in the regions file
    
    # Step 3: Update region_id in region-divisions.json
    for division in divisions_data['region_divisions']:
        old_region_id = division['region_id']
        if old_region_id in region_id_map:
            division['region_id'] = region_id_map[old_region_id]
    
    # Step 4: Sort divisions alphabetically by `name.en`
    divisions_data['region_divisions'] = sorted(
        divisions_data['region_divisions'], key=lambda x: x['name']['en']
    )
    
    # Step 5: Update division IDs sequentially
    for i, division in enumerate(divisions_data['region_divisions'], start=1):
        division['id'] = f"DIV_{str(i).zfill(3)}"
    
    # Save the sorted and updated regions.json
    with open(output_regions_file, 'w', encoding='utf-8') as f:
        json.dump({"regions": sorted_regions}, f, ensure_ascii=False, indent=4)
    
    # Save the sorted and updated region-divisions.json
    with open(output_divisions_file, 'w', encoding='utf-8') as f:
        json.dump(divisions_data, f, ensure_ascii=False, indent=4)


# Input and output file paths
input_regions_file = './data/regions.json'
input_divisions_file = './data/region-divisions.json'
output_regions_file = './data/regions.json'
output_divisions_file = './data/region-divisions.json'

# Run the sorting and formatting function
sort_and_update_ids(input_regions_file, input_divisions_file, output_regions_file, output_divisions_file)
