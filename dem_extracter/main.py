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

def output_file(lichi_df,output_path,new_alt ,x_coord, y_coord, elev):
    
    
    # 將elevation替換成new_alt
    lichi_df['altitude(m)'] = new_alt

    # 將elev, xcords, ycords 加入新的csv中
    lichi_df['elev'] = elev
    lichi_df['3826_x_coords'] = x_coord
    lichi_df['3826_y_coords'] = y_coord

    lichi_df.to_csv(output_path, index=False)
    print(f"Output saved to {output_path}")

def main(args=None):

    # 命令列參數設定

    parser = argparse.ArgumentParser(description="input files to revise flight hight from lichi mission.")
    parser.add_argument('dem_file', type=str, help="Path to the DEM file")
    parser.add_argument('csv_path', type=str, help="path to csv files")

    ## 程式import調用設定
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    
    # 將csv檔案轉換成geodataframe，wgs84轉換成epsg3826

    import trans
        
    '''
    Input: csv_path
    Output: xccord, ycoord, alt
    '''
    csvpath = args.csv_path
    geo_df,lichi_df  = trans.trans_input(csvpath)
    x_coord, y_coord =  trans.WGS84toEPSG4326(geo_df) ## 輸出格式為list
    alt = geo_df["alt"].tolist() # 輸出格式為list

    # 透過dem資料修正航高

    '''
    Input: dem_path, x_coord, y_coord, alt
    Output: elev,new_alt
    '''

    from extract_dem import extracter as ex
    
    dem_path = args.dem_file
    elev,new_alt = ex(dem_path,x_coord,y_coord,alt)


    # 設定匯出路徑
    '''
    Input: csv_path, filename
    Output: output_path
    '''
    filename = input("please insert filename for the output file (example: 'answer_data.csv'):")
    output_path = set_output_path(csvpath,filename)


    # 匯出檔案
    # lichi_df  原檔
    output_file(lichi_df,output_path,new_alt ,x_coord, y_coord, elev)

if __name__ == '__main__':
    main()



