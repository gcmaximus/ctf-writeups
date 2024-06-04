import pandas as pd
import folium
import re

# Example metadata (usually this would be read from files or an actual data source)

with open('exiftool', 'r') as f:
    content = f.read().split('====== ')[1:]



metadata = []

for i in content:
    dict = {}
    dict['filename'] = i.split('\n')[0]
    position = i.split('GPS Position                    : ')[1].split('\n')[0].replace(' deg', '°')
    print(dict)
    print(position)
    # input()
    dict['latitude'] = position.split(',')[0].strip()
    dict['longitude'] =  position.split(',')[1].strip()
    metadata.append(dict)
    
print(metadata)

# metadata = [
#     {"filename": "money_bag_992.png", "latitude": "39° 18' 50.25\" N", "longitude": "144° 41' 11.46\" W"},
#     {"filename": "money_bag_993.png", "latitude": "21° 35' 7.36\" S", "longitude": "80° 57' 46.08\" E"},
#     {"filename": "money_bag_994.png", "latitude": "24° 42' 57.13\" S", "longitude": "71° 38' 49.70\" E"},
#     {"filename": "money_bag_995.png", "latitude": "23° 22' 46.94\" S", "longitude": "71° 12' 39.69\" E"},
#     {"filename": "money_bag_996.png", "latitude": "17° 58' 6.67\" S", "longitude": "74° 15' 12.74\" E"},
#     {"filename": "money_bag_997.png", "latitude": "19° 48' 48.27\" S", "longitude": "84° 11' 58.80\" E"},
#     {"filename": "money_bag_998.png", "latitude": "34° 11' 29.50\" N", "longitude": "39° 39' 25.53\" W"},
#     {"filename": "money_bag_999.png", "latitude": "31° 34' 32.90\" N", "longitude": "39° 17' 56.07\" W"}
# ]

# def dms_to_decimal(dms_str):
#     dms_pattern = re.compile(r'\d+ deg \d+\u2019 \d+\.\d+\" [NSWE]')
#     match = dms_pattern.match(dms_str.strip())
#     if not match:
#         raise ValueError(f"Invalid DMS format: {dms_str}")
    
#     degrees, minutes, seconds, direction = match.groups()
#     degrees, minutes, seconds = float(degrees), float(minutes), float(seconds)
    
#     decimal = degrees + minutes / 60 + seconds / 3600
#     if direction in ['S', 'W']:
#         decimal *= -1
#     return decimal

import re
def dms_to_decimal(thing):
    deg, minutes, seconds, direction =  re.split('[°\'"]', thing)
    print((float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1))
    return (float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1)



def extract_coordinates(metadata):
    data = []
    for entry in metadata:
        lat = dms_to_decimal(entry['latitude'])
        lon = dms_to_decimal(entry['longitude'])
        data.append({"filename": entry["filename"], "latitude": lat, "longitude": lon})
    return pd.DataFrame(data)

# Convert metadata to a DataFrame
df = extract_coordinates(metadata)

# Create a folium map centered around the mean coordinate
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=2)

# Add points to the map
for index, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['filename']).add_to(m)

# Save the map to an HTML file
m.save('map.html')

# Optionally display the map directly in a Jupyter Notebook
# m
