
# needed package

import argparse
import sys
from osgeo import gdal
import pandas as pd

# input format

def extractElevation(path:str,x_coords:list[float],y_coords:list[float])->list[float|int]:
    '''
    this methon can sample the values from DEM for given points.
    
    Parameters:
    -----
    path:str path of DEM dataset
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
        src_ds = gdal.Open(path)
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
def convertToTerrain(elev,orignal_dem,extracted_dem):
    # elev 原始飛行高度,list
    # orignal_dem 原始dem,list
    new_elev = []
    for i in range(0,len(elev)):
        delta_hight = extracted_dem[i] - orignal_dem[i]
        elev[i] = elev[i] + delta_hight
        new_elev.append(elev[i]) ## calculate difference between orignal hight dem and way pts
    
    return new_elev # list

def csv_to_list(csv_path:str)->list:
    '''
    this function can read csv file and return a list of data

    Parameters:
    -----
    csv_path:str path of csv file

    Output:
    -----
    data:list list of data
    '''
    pts = pd.read_csv(csv_path)
    x_coords = pts['x'].tolist()
    y_coords = pts['y'].tolist()
    elev = pts['elev'].tolist()
    orignal_dem = pts['dem'].tolist()
    return x_coords,y_coords,elev,orignal_dem




def main(args=None):
    
    parser = argparse.ArgumentParser(description="Extract elevation from DEM and add to points CSV.")
    parser.add_argument('dem_file', type=str, help="Path to the DEM file")
    parser.add_argument('csv_path', type=str, help="path to csv files")
    parser.add_argument('output_path', type=str, help="path to save csv files")

    # 當args並不是用命令列開啟時，透過輸入args自訂參數

    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)
    


    # read csv
    x_coords,y_coords,elev,orignal_dem = csv_to_list(args.csv_path)
    
    ## return x_coords,y_coords,elev,orignal_dem

    extracted_dem = extractElevation(args.dem_file,x_coords,y_coords)
    
    # return a list of extracted_dem

    new_elev = convertToTerrain(elev,orignal_dem,extracted_dem)
    #return a list of revised elev
    
    data = list(zip(x_coords, y_coords, elev, orignal_dem))
    answer_df = pd.DataFrame(data, columns=['x_coords', 'y_coords', 'elev', 'orignal_dem'])

    answer_df['elev'] = new_elev
    answer_df['extracted_dem'] = extracted_dem 
    output_path = args.output_path
    answer_df .to_csv(output_path, index=False)
    print(f"Output saved to {output_path}")


if __name__ == "__main__":
    main()





