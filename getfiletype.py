from config import LEGAL_TYPE, LEGAL_CLASSES_TYPE

def filetype(func):
    def wrapper(filename):
        typelist = filename.split('_')
        if typelist[-1] != '按更新类型统计.xls' or len(typelist) != 5:
            return
        if typelist[1][0:2] not in LEGAL_TYPE or typelist[3][2:4] not in LEGAL_CLASSES_TYPE:
            return
        type_str = typelist[1][0:2] + typelist[3][2:4]
        return func(filename = filename, typestr = type_str)
    return wrapper

@filetype
def test(*arg, **karg):
    print(karg)

if __name__ == "__main__":
    test(r'2018年度数据统计结果0525\2018年数据_建设耕地汇总_全国各省_国家利用等_按更新类型统计.xls')