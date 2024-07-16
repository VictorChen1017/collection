import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def WGS84toEPSG4326(geo_df)->list:
    '''
    this method can convert WGS84 to EPSG4326
    
    Parameters:
    -----
    x:float x_coordinate
    y:float y_coordinate
    
    Output
    -----
    x_coords: a list of x_coordinate
    y_coords: a list of y_coordinate


    Reference
    -----
    https://gis.stackexchange.com/questions/58538/converting-projected-coordinates-to-lat-lon-using-python
    '''
    geometry = [Point(xy) for xy in zip(geo_df["lon"], geo_df["lat"])] # 表示方式與3826相反
    pt = gpd.GeoDataFrame(geo_df, geometry=geometry) # create geodataframe
    pt.set_crs(epsg=4326, inplace=True)
    pt_3826 = pt.to_crs(epsg=3826) # convert to epsg 3826

    pt_3826_x = [point.x for point in pt_3826['geometry']]
    pt_3826_y = [point.y for point in pt_3826['geometry']]
    print("Transform successfully")
    return pt_3826_x, pt_3826_y

# 在主程式就先把lichi 做成geodf 

def trans_input(csvpath):
    lichi_df = pd.read_csv(csvpath)
    geo_df = lichi_df.iloc[:,0:3]
    geo_df = geo_df.rename(columns={"latitude": "lat", "longitude": "lon", "altitude(m)": "alt"})
    print("Input waypoint successfully")
    return geo_df
    

'''
csvpath = lichi_example.csv
geo_df = trans_input(csvpath)
x_coord, y_coord =  WGS84toEPSG4326(geo_df)
print(x_coord)
print(y_coord)

'''