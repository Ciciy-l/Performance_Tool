# -*- coding: UTF-8 -*-
import math

from com.excelOperation import ExcelOperations
from com.common import read_config, get_xlsx_filenames_list, basic_directory_detection


def generate_performance_table():
    """
    生成绩效合约
    """
    # 检测必要目录是否存在，如不存在则创建
    basic_directory_detection()
    # 实例化考核条目维护表操作对象
    performance_item_table = ExcelOperations(read_config("path").get("performance_item_table_path"))
    # 获取存在考核条目的岗位列表
    item_job_list = performance_item_table.get_sheet_list()
    # 实例化template表格
    template_tabel = ExcelOperations(read_config("path").get("performance_template_path"))
    # 获取存在模板的岗位列表
    template_job_list = template_tabel.get_sheet_list()

    for item_job in item_job_list:
        for template_job in template_job_list:
            if item_job == template_job:
                # 切换到当前岗位对应的模板sheet
                ws = template_tabel.switch_sheet(item_job)
                # 获取当前岗位有效考核项目数据
                valid_items_datas = []
                [valid_items_datas.append(key_value) for key_value in
                 performance_item_table.get_sheet_data(item_job) if key_value.get("是否生效") == 1]
                # TODO 按类别自动将数据排序
                # 获取当前岗位考核项目数量
                items_num = len(valid_items_datas)
                # 获取新行插入位置
                position = int(read_config("insert_position").get(item_job))
                # 替换时间标签
                template_tabel.replacing_labels_in_regions(item_job)
                # 在新行中写入数据
                line = 0
                for row in ws.iter_rows(min_row=position, max_row=position + items_num - 1, min_col=1,
                                        max_col=len(valid_items_datas[0]) - 1):
                    data = valid_items_datas[line]
                    for cell, value in zip(row, data.values()):
                        cell.value = value
                    line += 1
                # 生成绩效考核表到指定目录
                template_tabel.save_wb("{}{}.xlsx".format(read_config("path").get("performance_folder_path"), item_job))
                # 打开生成的表格
                new = ExcelOperations("{}{}.xlsx".format(read_config("path").get("performance_folder_path"), item_job))
                # 删除生成表格中的其他sheet
                try:
                    [new.delete_sheet(sheet) for sheet in new.get_sheet_list() if sheet != item_job]
                except KeyError:
                    pass
                # 获取对应模板中预留空行数量
                blank_rows = int(read_config("template_blank_rows").get(item_job))
                # 合并类别与权重列单元格
                new.merge_similar_cells_by_column([1, position, position + items_num - 1], item_job, next_col=True)
                # 隐藏多余空行
                new.hidden_data_lines(position + items_num, blank_rows - items_num, item_job)
                # 保存生成的表格
                new.save_wb()
                # 关闭模板文件
                template_tabel.close_wb()


def summary_performance_table():
    # 获取datas目录下xlsx文件名列表
    table_list = get_xlsx_filenames_list(read_config("path").get("performance_summary_data_path"))
    # 遍历获取每个表格的数据
    for table in table_list:
        # 实例化当前表格操作对象
        current_table = ExcelOperations(table)
        # 按行获取sheet数据
        current_table_lines = current_table.get_sheet_datalines()
        # 获取字段表头所在位置
        # key_position =


if __name__ == '__main__':
    generate_performance_table()
    # summary_performance_table()
