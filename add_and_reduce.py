import os
import numpy as np
import pandas as pd

from config import RESULT_FILE_PATH, CLASSES_GRADE

class AddAndReduce:
    def __init__(self, df, typestr):
        self.dataframe = df
        self.typestr = typestr
        self.writer = pd.ExcelWriter(os.path.join(RESULT_FILE_PATH, self.typestr + '.xls'))
        self.keyword = ['行政区划代码', '行政区划名称']

    def __del__(self):
        self.writer.close()

    def write_distribution(self):
        farmland_grade_frame = self.dataframe.drop(self.keyword + ['平均等', '分区'], axis = 1)
        farmland_grade_sum = pd.DataFrame(farmland_grade_frame.sum(),columns = ['面积(公顷)'])
        farmland_grade_sum['面积(亩)'] = farmland_grade_sum['面积(公顷)'] * 15
        farmland_grade_sum['比例'] = farmland_grade_sum['面积(公顷)'] / farmland_grade_sum['面积(公顷)']['总计']
        farmland_grade_sum.to_excel(excel_writer = self.writer, sheet_name = '分级统计')
        self.writer.save()
        self.write_distribution_groupby_grade(farmland_grade_sum)
        # 历史遗留问题，实为冗余调用，下个版本考虑去除

    def write_distribution_groupby_grade(self, souce_farmland_grade_sum, axis = 0):
        farmland_grade_sum = souce_farmland_grade_sum.copy()
        if axis == 1:
            farmland_grade_sum.loc['耕地等级'] = CLASSES_GRADE
            farmland_area_grade_sum = farmland_grade_sum.groupby(CLASSES_GRADE, sort = False, axis = 1).sum()
            farmland_area_grade_droped = farmland_area_grade_sum.drop(['耕地等级'], axis = 0)
            for key in farmland_area_grade_droped.keys():
                farmland_area_grade_droped[key + '占比'] = farmland_area_grade_droped[key] / farmland_area_grade_droped[key]['合计']
            farmland_area_grade_droped.to_excel(excel_writer = self.writer, sheet_name = '分地区分级统计-行')
        elif axis == 0:
            farmland_grade_sum['耕地等级'] = CLASSES_GRADE
            farmland_grade_sum.groupby('耕地等级', sort = False).sum().to_excel(excel_writer = self.writer, sheet_name = '分地区分级统计-列')
        self.writer.save()

    def write_distribution_groupby_area(self):
        farmland_area_frame = self.dataframe.drop(self.keyword + ['平均等'], axis = 1)
        farmland_area_sum = farmland_area_frame.groupby('分区', sort = False).sum()
        farmland_area_sum.loc['合计'] = farmland_area_sum.apply(lambda x:x.sum(), axis = 0)
        self.write_distribution_groupby_grade(farmland_area_sum, axis = 1)

        farmland_area_sum['平均等'] = self.get_average_grade()
        if '利用' in self.typestr:
            farmland_area_sum['产能(万吨)'] = (0.002325 - farmland_area_sum['平均等'] * 0.00015) * farmland_area_sum['总计']
            farmland_area_sum['产能(万吨)']['合计'] = farmland_area_sum['产能(万吨)'].sum()
        farmland_area_sum.loc['合计百分比'] = farmland_area_sum.loc['合计'][0 : 16] / farmland_area_sum.loc['合计']['总计']
        farmland_area_sum.to_excel(excel_writer = self.writer, sheet_name = '分地区统计')
        self.writer.save()

    def get_average_grade(self):
        farmland_area_frame = self.dataframe.drop(self.keyword, axis = 1)
        def wavg(group, avg_name, weight_name):
            value = group[avg_name]
            weight = group[weight_name]
            try:
                return (value * weight).sum() / weight.sum()
            except ZeroDivisionError:
                return np.nan
        return farmland_area_frame.groupby("分区").apply(wavg, '平均等', '总计')

def pivot_table(df, typestr):
    cla = AddAndReduce(df, typestr)
    cla.write_distribution()
    cla.write_distribution_groupby_area()