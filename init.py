import os
import numpy as np
import pandas as pd

from config import RAW_FILE_PATH
from getfiletype import filetype

@filetype
def analyse(*arg, **karg):
    dataframe = pd.read_excel(karg['filename'])
    if '时段' in dataframe.keys():
        if '建设' not in karg['typestr']:
            raise Exception("数据表格式与预设不符，‘时段’字段应只出现在建设耕地表中")
        print('进入建设')
        pass
    else:
        print('进入新增减少')


def init():
    files= os.listdir(RAW_FILE_PATH)
    for file in files:
        if not os.path.isdir(file):
            file_path = os.path.join(RAW_FILE_PATH, file)
            analyse(file_path)


if __name__ == '__main__':
    init()