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

def set_output_path(dir_path,filename=None): # 必田參數在前，選填參數在後
    if filename:
        # Check if the filename ends with .csv
        if not filename.endswith('.csv'):
            filename = filename + '.csv'
            #print("auto add .csv")

        output_dir = os.path.dirname(dir_path) # 需要解決路徑問題
        costom_path = os.path.join(output_dir, filename) # 預設檔名與csvfile相同
        # 自訂路徑功能目前尚未添加
        output_path = costom_path
        #print("create costom filename")
    else:
        # Default to the same directory as csvpath
        output_path = os.path.dirname(dir_path)
        # Ensure the output path ends with a directory separator
        output_path = os.path.join(output_path, 'answer_data.csv')
        #print("create default filename")
    
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
    output_path = set_output_path(csvpath,filename)

    a = [args.dem_file,args.csv_path,output_path]
    extract_dem_main(a)

'''
if __name__ == "__main__"
    main()
'''

dem = r"C:\Users\USER\Documents\GitHub\collection\dem_extracter\test_data\Dali_2m_H.tif"
csvpath = r"C:\Users\USER\Documents\GitHub\collection\dem_extracter\test_data\lichi_example.csv"

aa = [dem,csvpath]
main(aa)

