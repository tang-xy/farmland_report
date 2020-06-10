import os
import numpy as np
import pandas as pd

from config import RAW_FILE_PATH, province, area
from getfiletype import filetype
import add_and_reduce 
import build_use 

@filetype
def analyse(*arg, **karg):
    dataframe = pd.read_excel(karg['filename'])
    if '行政区划名称' in dataframe.keys():
        dataframe['分区'] = dataframe['行政区划名称']
        dataframe['分区'].replace(province, area, inplace=True)
    else:
        raise Exception("数据表格式与预设不符, 缺少省级的‘行政区划名称’字段")
    if '时段' in dataframe.keys():
        if '建设' not in karg['typestr']:
            raise Exception("数据表格式与预设不符，‘时段’字段应只出现在建设耕地表中")
        print('进入建设')
        build_use.pivot_table(dataframe, karg['typestr'])
    else:
        print('进入新增减少')
        add_and_reduce.pivot_table(dataframe, karg['typestr'])


def init():
    files= os.listdir(RAW_FILE_PATH)
    for file in files:
        if not os.path.isdir(file):
            file_path = os.path.join(RAW_FILE_PATH, file)
            analyse(file_path)


if __name__ == '__main__':
    init()