# -*- coding: UTF-8 -*-

from com.excelOperation import ExcelOperations
from com.common import read_config

if __name__ == '__main__':
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
                # 获取当前岗位考核项目数量
                items_num = len(valid_items_datas)
                # 获取新行插入位置
                position = int(read_config("insert_position").get(item_job))
                # 模板中插入新行
                template_tabel.insert_blank_line(position, items_num)
                # 在新行中写入数据
                line = 0
                for row in ws.iter_rows(min_row=position, max_row=position + items_num - 1, min_col=1,
                                        max_col=len(valid_items_datas[0])):
                    data = valid_items_datas[line]
                    for cell, value in zip(row, data.values()):
                        cell.value = value
                    line += 1
                # 生成绩效考核表到指定目录
                template_tabel.save_wb("{}{}.xlsx".format(read_config("path").get("performance_folder_path"), item_job))
                # 关闭模板文件
                template_tabel.close_wb()


