## Introduction
This is a tool for revise hight for the lichi UAV mission

<br>needed file as follow:

**dem.tif** ：a DEM(Digital Elevation/Terrain Model) file contains your mission area, file formet: .tif

**waypoints.csv** ：your mission waypoints calculated by [lichi](https://cc8.pl/download/atomicmapper.html) 

## Environments

python library:
- os, argparse, sys 
- pandas, gdal, geopandas, shapely

## Usage

```console
python main.py dem.tif waypoints.csv
```

you may enter your file name as:
<br>"please insert filename for the output file (example: 'answer_data.csv'):"
<br>your file will saved in test_data folder
