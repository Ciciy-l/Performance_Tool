# -*- coding: UTF-8 -*-
import os
import sys

from com.excelOperation import ExcelOperations
from com.common import read_config, get_xlsx_filenames_list, basic_directory_detection


def exception_permission_file(func):
    def run():
        try:
            func()
        except PermissionError as e:
            msg = "文件 {} 已被占用，请关闭后重试!".format(os.path.abspath(str(e).split(":")[-1].strip().strip("/").strip("'")))
            return msg

    return run


@exception_permission_file
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
                insert_position = read_config("insert_position")
                if insert_position.get(item_job):
                    position = int(insert_position.get(item_job))
                else:
                    position = int(insert_position.get("default"))
                # 替换文本标签
                template_tabel.replacing_labels_in_regions()
                # 替换时间标签
                template_tabel.replacing_labels_in_regions(item_job, mode="time")
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
                template_blank_rows = read_config("template_blank_rows")
                if template_blank_rows.get(item_job):
                    blank_rows = int(template_blank_rows.get(item_job))
                else:
                    blank_rows = int(template_blank_rows.get("default"))
                # 合并类别与权重列单元格
                new.merge_similar_cells_by_column([1, position, position + items_num - 1], item_job, next_col=True)
                # 隐藏多余空行
                new.hidden_data_lines(position + items_num, blank_rows - items_num, item_job)
                # 保存生成的表格
                new.save_wb()
                # 关闭模板文件
                template_tabel.close_wb()


@exception_permission_file
def summary_performance_table():
    """
    汇总绩效表并统计
    """
    # 检测必要目录是否存在，如不存在则创建
    basic_directory_detection()
    # 获取datas目录下xlsx文件名列表
    table_list = get_xlsx_filenames_list(read_config("path").get("performance_summary_data_path"))
    # 初始化结果汇总列表
    result_list = []
    index = 1
    # 遍历获取每个表格的数据
    for table in table_list:
        # 实例化当前表格操作对象(以读取值模式打开)
        current_table = ExcelOperations(table, get_func_data=True)
        # 按行获取sheet数据
        current_table_lines = current_table.get_sheet_datalines()
        # 初始化分析说明加分项存放列表
        analysis_description_add_list = []
        # 初始化分析说明扣分项存放列表
        analysis_description_subtract_list = []
        # 初始化结果变量
        personnel_name = ""
        final_score = ""
        analysis_description_text = ""
        # 初始化row_id
        row_id = 1
        # 遍历行获取所需数据
        for line in current_table_lines:
            # print(line)
            personnel_job = ""
            if line[0] and isinstance(line, list):
                # 获取岗位与姓名
                if " 被考评人" in line[0]:
                    # 获取岗位信息
                    s_index = line[0].find("岗位")
                    e_index = line[0].find("部门")
                    personnel_job = line[0][s_index:e_index].strip("岗位").strip("部门").strip(" ").strip("：")
                    # 获取姓名信息
                    s_index = line[0].find("被考评人：")
                    e_index = line[0].find("直接上级：")
                    personnel_name = line[0][s_index:e_index].strip("被考评人").strip(" 直接上级").strip(" ").strip("：")
                # 获取最终得分
                elif "最后评分" in line[0]:
                    final_score = line[0][line[0].find("=") + 1:]
            # 获取当前岗位的考核项目起始行号
            insert_position = read_config("insert_position")
            if personnel_job:
                if insert_position.get(personnel_job):
                    start_row = insert_position.get(personnel_job)
                else:
                    start_row = insert_position.get("default")
            else:
                start_row = insert_position.get("default")
            # 获取并汇总分析说明
            if line[-1] and isinstance(line, list) and row_id >= int(start_row):
                # 获取当前分析说明内容
                text = str(line[-1])
                # 判断是加分项还是扣分项，存入相应列表
                if "加分" in text:
                    analysis_description_add_list.append(text.strip("加分项").strip(" ").strip("：").strip(":"))
                elif "扣分" in text:
                    analysis_description_subtract_list.append(text.strip("扣分项").strip(" ").strip("：").strip(":"))
                analysis_description_add_text = "；".join(analysis_description_add_list)
                analysis_description_subtract_text = "；".join(analysis_description_subtract_list)
                analysis_description_add = []
                analysis_description_subtract = []
                if analysis_description_add_text:
                    analysis_description_add = ["加分项：" + analysis_description_add_text + "。"]
                if analysis_description_subtract_text:
                    analysis_description_subtract = ["扣分项：" + analysis_description_subtract_text + "。"]
                analysis_description_text = "\n".join(analysis_description_add + analysis_description_subtract)
            row_id += 1
        # 无加分项或扣分项时，将分析说明文本设为"无加减分项目。"
        if not analysis_description_add_list and not analysis_description_subtract_list:
            analysis_description_text = "无加减分项目。"
        # print(personnel_job, personnel_name, final_score, analysis_description_text)
        result_list.append([index, personnel_name, final_score, analysis_description_text])
        index += 1
        # 关闭当前表格
        current_table.close_wb()
    # print(result_list)

    # 实例化summary_template表格
    template_tabel = ExcelOperations(read_config("path").get("performance_summary_template_path"))
    # 获取汇总条目数量
    item_num = len(result_list)
    # 获取新增条目插入起始行号
    position = int(read_config("summary_insert_position").get("汇总新增条目起始行"))
    # 替换文本标签
    template_tabel.replacing_labels_in_regions()
    # 替换时间标签
    template_tabel.replacing_labels_in_regions(mode="time")
    # 切换到当前活动sheet
    ws = template_tabel.switch_sheet()
    # 开始写入数据
    index = 0
    for row in ws.iter_rows(min_row=position, max_row=position + item_num - 1, min_col=1, max_col=len(result_list[0])):
        for cell, value in zip(row, result_list[index]):
            cell.value = value
        index += 1
    # 获取汇总模板中预留空行数量
    blank_rows = int(read_config("summary_template_blank_rows").get("汇总模板预留空行数"))
    # 隐藏多余行
    template_tabel.hidden_data_lines(position + item_num, blank_rows - item_num)
    # 生成绩效考核表到指定目录
    template_tabel.save_wb(read_config("path").get("performance_summary_result_path"))
    # 关闭模板文件
    template_tabel.close_wb()


if __name__ == '__main__':
    # 命令行运行
    if len(sys.argv[1:]) == 1:
        # 获取参数
        arg = sys.argv[1]
        if arg == "-generate":
            result_info = generate_performance_table()
            print("已生成各岗位绩效合约至{}".format(os.path.abspath(read_config("path").get("performance_folder_path"))))
            print(result_info) if result_info else None
        elif arg == "-summary":
            result_info = summary_performance_table()
            print("已汇总人员绩效结果至{}".format(os.path.abspath(read_config("path").get("performance_summary_result_path"))))
            print(result_info) if result_info else None
        os.system('pause')
    else:
        print("""缺少运行参数！
    -generate 生成绩效合约
    -summary 汇总绩效结果
或在当前目录下直接运行 generate.bat 与 summary.bat
""")
        os.system('pause')

    # result_info = generate_performance_table()
    # result_info = summary_performance_table()
    # print(result_info) if result_info else None
