import json

def generate_all_json(regions_file, divisions_file, communes_file, output_file):
    # Load regions.json
    with open(regions_file, 'r', encoding='utf-8') as f:
        regions_data = json.load(f)

    # Load region-divisions.json
    with open(divisions_file, 'r', encoding='utf-8') as f:
        divisions_data = json.load(f)

    # Load communes.json
    with open(communes_file, 'r', encoding='utf-8') as f:
        communes_data = json.load(f)

    # Create a mapping of divisions and their communes
    division_commune_map = {}
    for commune in communes_data['communes']:
        division_id = commune['region_division_id']
        if division_id not in division_commune_map:
            division_commune_map[division_id] = []
        division_commune_map[division_id].append(commune)

    # Create a mapping of regions and their divisions
    region_tree = []
    region_division_map = {}

    # Group divisions by region_id
    for division in divisions_data['region_divisions']:
        region_id = division['region_id']
        division_id = division['id']
        
        # Attach communes to the division
        division['communes'] = division_commune_map.get(division_id, [])
        
        if region_id not in region_division_map:
            region_division_map[region_id] = []
        region_division_map[region_id].append(division)

    # Build the tree structure
    for region in regions_data['regions']:
        region_id = region['id']
        region_tree.append({
            "id": region_id,
            "name": region['name'],
            "divisions": region_division_map.get(region_id, [])  # Attach divisions to the region
        })

    # Save the hierarchical tree as all.json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"regions": region_tree}, f, ensure_ascii=False, indent=4)

# Input and output file paths
input_regions_file = './data/regions.json'
input_divisions_file = './data/region-divisions.json'
input_communes_file = './data/communes.json'
output_all_file = './data/all.json'

# Generate the hierarchical JSON
generate_all_json(input_regions_file, input_divisions_file, input_communes_file, output_all_file)
