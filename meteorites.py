import folium
import json
import pandas as pd
import numpy as np

with open('metorites.json') as f:
    data = json.load(f)
    
print(f)

#transforming JSON to CSV
df = pd.DataFrame.from_dict(data, orient='columns') 

#Dropping NaN values from Latitude and Longitude
df = df.dropna(subset=['reclat', 'reclong'])

#Selecting only Latitude
lat = list(df['reclat'])

#Selecting only Longitude
lon = list(df['reclong'])

#Selecting only names
name = list(df['name'])


#creating map Object
map = folium.Map(location=[37.0902, -95.7129], zoom_start=1, min_zoom=2,titles="Mapbox Bright",fill_opacity=0.7)

#feature group
fgm = folium.FeatureGroup(name="Metorites")

#for loop to add all values from the csv file
for lt,ln , nm in zip(lat,lon,name):
	fgm.add_child(folium.CircleMarker(location=[lt,ln], radius= 6, popup=nm, color='brown', fill_color='red'))


fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding="utf-8-sig").read(),
	style_function=lambda x:{'fillColor':'green' if x ['properties']['POP2005']<10000000 
	else 'orange' if 10000000 <= x['properties']['POP2005']< 20000000 else 'red'}))


#Creating Layer control
map.add_child(fgp)
map.add_child(fgm)
map.add_child(folium.LayerControl())


#creating the HTML map
map.save("Map1.html")