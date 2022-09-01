from com.excelOperation import ExcelOperations
from com.common import read_config

if __name__ == '__main__':
    performance_item_table = ExcelOperations(read_config("path").get("performance_item_table_path"))
    # print(performance_item_table.get_sheet_list())
    print(performance_item_table.get_sheet_data("测试岗位1"))
