
from map import MapInfo

map_index = 1
input_file = '/res/map/map' + str(map_index)
output_file = '/res/map' + str(map_index) + '.tmx'

template="""
<?xml version="1.0" encoding="UTF-8"?>
<map version="1.10" tiledversion="1.11.0" orientation="orthogonal" renderorder="left-down" width="WIDTH_PLACEHOLDER" height="HEIGHT_PLACEHOLDER" tilewidth="24" tileheight="24" infinite="0" nextlayerid="5" nextobjectid="1">
 <tileset firstgid="1" source="t1.tsx"/>
 <layer id="1" name="grass" width="20" height="20">
  <data encoding="csv">
  DATA_PLACEHOLDER
</data>
 </layer>
</map>
"""

with open(input_file, 'r') as f:
    data = f.read().split(',')
width, height = MapInfo().get_map_size(map_index)
data = [data[i:i+width] for i in range(0, len(data), width)]
data = '\n'.join([','.join(row) for row in data])
output = template.replace('WIDTH_PLACEHOLDER', str(width)).replace('HEIGHT_PLACEHOLDER', str(height)).replace('DATA_PLACEHOLDER', data)
with open(output_file, 'w') as f:
    f.write(output)