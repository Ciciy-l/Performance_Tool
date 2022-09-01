from openpyxl import load_workbook


class ExcelOperations:

    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.wb = load_workbook(self.excel_path)

    def get_sheet_list(self, list_type="name"):
        '''
        获取sheet名称或对象列表
        :param list_type:"name"返回名称列表，"obj"返回对象列表
        '''
        sheet_list = []
        if list_type == "name":
            for sheet in self.wb.sheetnames:
                sheet_list.append(sheet)
        elif list_type == "obj":
            for sheet in self.wb:
                sheet_list.append(sheet)
        return sheet_list

    def get_sheet_data(self, sheet_name: str):
        '''
        传入sheet名称，将每行的数据以字典的形式获取，并放在字典中返回
        :param sheet_name: sheet名称
        '''
        sheet_obj = self.wb[sheet_name]
        key_tuple = sheet_obj[1]
        key_list = []
        sheet_data_list = []
        [key_list.append(key_cell.value) for key_cell in key_tuple]
        row_id = 0
        for row in sheet_obj.iter_rows(min_row=2, max_row=sheet_obj.max_row):
            value_list = []
            data_dict = {}
            [value_list.append(cell.value) for cell in row]
            [data_dict.update({key: value}) for key, value in zip(key_list, value_list)]
            sheet_data_list.append(data_dict)
        return sheet_data_list
