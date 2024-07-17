
# needed package

import argparse
import sys
from osgeo import gdal
import pandas as pd

# input format

def extractElevation(dem_path:str,x_coords:list[float],y_coords:list[float])->list[float|int]:
    '''
    this methon can sample the values from DEM for given points.
    
    Parameters:
    -----
    dem_path:str path of DEM dataset
    x_coords:list[float] x_coordinates of points
    y_coords:list[float] y_coordinates of points

    Output
    -----
    elev:list[float|int] list of elevation extract results
    
    Reference
    -----
    https://gis.stackexchange.com/questions/225370/get-individual-pixel-values-on-a-raster-image-using-gdal-and-python
    https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#get-raster-band

    '''
    # this allows GDAL to parse raster datasets
    gdal.UseExceptions()
    try:
        src_ds = gdal.Open(dem_path)
    except RuntimeError as e:
        print('Unable to open INPUT.tif')
        print(e)
        sys.exit(1)

    try:
        band = src_ds.GetRasterBand(1)
    except RuntimeError as e:
        # for example, try GetRasterBand(10)
        print(e)
        sys.exit(1)

    # get the image size and raster information by GDAL

    geotransform = src_ds.GetGeoTransform() 
    ## format：(296110.0, 20.0, 0.0, 2789170.0, 0.0, -20.0) 
    ## top left x, pixel size , rotation,  top left y, pixel size , rotation

    band = src_ds.GetRasterBand(1)
    xOrigin = geotransform[0]
    yOrigin = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]

    elev = [] 
    ## storage elevation result

    # extract elevation from DEM, for each point

    for i in range(len(x_coords)): # number of data
        x = x_coords[i]
        y = y_coords[i]
        # compute pixel offset
        xOffset = int((x - xOrigin) / pixelWidth)
        yOffset = int((y - yOrigin) / pixelHeight)
        # get individual pixel values
        data = band.ReadAsArray(xOffset, yOffset, 1, 1)
        value = data[0, 0]
        elev.append(value)
    
    return elev

# correct hight for the way points
def convertToTerrain(alt:list[float],elev:list[float])->list[float]:
    # alt 原始飛行高度,list
    # elev 地形高度,list
    new_alt = []
    for i in range(0,len(alt)):
        # 新高度=原高度+地形高度
        alt[i] = alt[i] + elev[i]
        new_alt.append(alt[i]) ## calculate difference between orignal hight dem and way pts
    
    return new_alt # list





def extracter(dem_path,x_coords,y_coords,alt):
    # dem_path: str, path to DEM file
    # x_coords: list[float], x coordinates of points
    # y_coords: list[float], y coordinates of points
    # alt: list[float], original flighthight of points
    
    # 處理匯入的dem資料，並且提取出對應的高度
    
    elev = extractElevation(dem_path,x_coords,y_coords)
    print("DEM Extract successfully")

    ## return elev

    new_alt = convertToTerrain(alt,elev)
    print("new_alt revise successfully")
    #return a list of revised elev
    return elev,new_alt
    





