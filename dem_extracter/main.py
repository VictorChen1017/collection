# main script
'''
this is the project for correcting hight from lichi mission

usage:
python main.py dem_file csv_file

'''
# needed package

import argparse
import pandas as pd
import os

# 設定結果的匯出路徑

def set_output_path(custom_path=None):
    if custom_path:
        # Use the user-defined path if provided
        output_path = custom_path
    else:
        # Default to the same directory as csvpath
        output_path = os.path.dirname(csvpath)
    
    # Ensure the output path ends with a directory separator
    output_path = os.path.join(output_path, 'answer_data.csv')
    
    return output_path



def main(args=None):

    parser = argparse.ArgumentParser(description="input files to revise flight hight from lichi mission.")
    parser.add_argument('dem_file', type=str, help="Path to the DEM file")
    parser.add_argument('csv_path', type=str, help="path to csv files")

    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)



    from extract_dem import main as extract_dem_main

    filename = input("please insert filename for the output file (example: 'answer_data.csv'):")
    if filename :
        output_dir = os.path.dirname(csvpath) # 需要解決路徑問題
        costom_path = os.path.join(output_dir, filename)
    else:
        costom_path = set_output_path() #預設路徑

    a = [args.dem_file,args.csv_path,costom_path]
    extract_dem_main(a)

'''
if __name__ == "__main__":
    main()
'''

dem = r"C:\Users\USER\Documents\GitHub\collection\dem_extracter\test_data\Dali_2m_H.tif"
csvpath = r"C:\Users\USER\Documents\GitHub\collection\dem_extracter\test_data\test_data.csv"
costom_path = r'C:\Users\USER\Documents\GitHub\collection\dem_extracter\test_data\costom_data.csv'
default_path = set_output_path()
aa = [dem,csvpath]
main(aa)

