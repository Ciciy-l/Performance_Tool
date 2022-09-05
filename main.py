# -*- coding: UTF-8 -*-

from com.excelOperation import ExcelOperations
from com.common import read_config

if __name__ == '__main__':
    # 实例化考核条目维护表操作对象
    performance_item_table = ExcelOperations(read_config("path").get("performance_item_table_path"))
    # 获取存在考核条目的岗位列表
    job_list = performance_item_table.get_sheet_list()
    performance_item_table.insert_blank_line(2, 2)
    print(performance_item_table.get_sheet_data("综合办主任"))
