import os
import numpy as np
import pandas as pd

from add_and_reduce import AddAndReduce
from config import RESULT_FILE_PATH 

class BuildUse(AddAndReduce):
    def __init__(self, df, typestr):
        self.dataframe_before = df[df['时段'] == '建设前'].drop(['时段'], axis = 1)
        self.dataframe_after = df[df['时段'] == '建设后'].drop(['时段'], axis = 1)
        self.typestr = typestr
        self.writer_before = pd.ExcelWriter(os.path.join(RESULT_FILE_PATH, self.typestr + '_建设前.xls'))
        self.writer_after = pd.ExcelWriter(os.path.join(RESULT_FILE_PATH, self.typestr + '_建设后.xls'))
        self.keyword = ['行政区划代码', '行政区划名称']
        self.write_distribution = self.build_decorator(super().write_distribution)
        self.write_distribution_groupby_area = self.build_decorator(super().write_distribution_groupby_area)
    
    def __del__(self):
        self.writer_before.close()
        self.writer_after.close()

    def build_decorator(self, func):
        def wrapper():
            self.writer = self.writer_before
            self.dataframe = self.dataframe_before
            func()
            self.writer = self.writer_after
            self.dataframe = self.dataframe_after
            func()
        return wrapper


def test(df):
    # cla = BuildUse(df)
    # print(cla.dataframe_before)
    pass

def pivot_table(df, typestr):
    cla = BuildUse(df, typestr)
    cla.write_distribution()
    cla.write_distribution_groupby_area()

if __name__ == "__main__":
    pass
