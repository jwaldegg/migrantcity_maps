import json
import csv

def edit_geojson(csv_file, geojson_file, output_file):
    # Read the CSV file
    data = {}
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            spatial_alias = row[0]
            score = int(row[1])
            data[spatial_alias] = score

    # Load the GeoJSON file
    with open(geojson_file, 'r') as f:
        geojson = json.load(f)

    # Iterate over the features in the GeoJSON
    for feature in geojson['features']:
        properties = feature['properties']
        spatial_alias = properties.get('spatial_alias')

        # Check if the spatial_alias exists in the CSV data
        if spatial_alias in data:
            score = data[spatial_alias]

            # Set the fill color based on the score
            if score == 1:
                properties['fill'] = '#fe0608'
            elif score == 2:
                properties['fill'] = '#ff3737'
            elif score == 3:
                properties['fill'] = '#fd6969'
            elif score == 4:
                properties['fill'] = '#e2e2e2'
            elif score == 5:
                properties['fill'] = '#c9fdc7'
            elif score == 6:
                properties['fill'] = '#9aff99'
            elif score == 7:
                properties['fill'] = '#6aff69'    

  
    # Save the modified GeoJSON file
    with open(output_file, 'w') as f:
        json.dump(geojson, f)


# Usage example
csv_file = 'berlin/example_berlin.csv'
geojson_file = 'berlin/berlin.geojson'
output_file = 'berlin/modified.geojson'

edit_geojson(csv_file, geojson_file, output_file)