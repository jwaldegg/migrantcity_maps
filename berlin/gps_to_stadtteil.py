import csv
import json
from geojson import Point, Polygon

def is_point_in_polygon(point, polygon):
    x, y = point['coordinates']
    exterior = polygon['coordinates'][0]
    n = len(exterior)
    inside = False

    p1x, p1y = exterior[0]
    for i in range(n+1):
        p2x, p2y = exterior[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y-p1y) * (p2x-p1x) / (p2y-p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def get_spatial_alias(gps_coordinates, geojson_file):
    with open(geojson_file) as f:
        data = json.load(f)

    features = data['features']
    for feature in features:
        polygon = feature['geometry']
        if polygon['type'] == 'Polygon':
            if is_point_in_polygon(gps_coordinates, polygon):
                return feature['properties']['spatial_alias']
        elif polygon['type'] == 'MultiPolygon':
            for subpolygon in polygon['coordinates']:
                if is_point_in_polygon(gps_coordinates, {'type': 'Polygon', 'coordinates': subpolygon}):
                    return feature['properties']['spatial_alias']

    return None  

def main():
    geojson_file = 'berlin/berlin.geojson'  # specify your file path here
    csv_file = 'berlin/gps.csv'  # specify your file path here
    csv_output_file = 'berlin/output_gps.csv'  # specify your file path here

    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f)
        data = list(csv_reader)

    with open(csv_output_file, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['STADTTEIL'])  # writing header

        for row in data[1:]:
            x, y = float(row[0]), float(row[1])  # assuming x and y are float numbers
            spatial_alias = get_spatial_alias({'type': 'Point', 'coordinates': [x, y]}, geojson_file)
            csv_writer.writerow([spatial_alias])

if __name__ == "__main__":
    main()
