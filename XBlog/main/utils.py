#!/usr/bin/env python
# encoding: utf-8

from xlrd import open_workbook
from xlutils.copy import copy

def xls_append(file_name, user_msg_lst):
    rb = open_workbook(file_name, formatting_info=True)
    r_sheet = rb.sheet_by_index(0)
    wb = copy(rb)
    w_sheet = wb.get_sheet(0)
    new_row = r_sheet.nrows
    vip_table = {
            'c': [u"初级会员", 1],
            'z': [u"中级会员", 12],
            'g': [u"高级会员", 36]
            }
    user_msg_lst.append(vip_table.get(user_msg_lst[2], [u"初级会员", 1])[1])
    user_msg_lst[2] = vip_table.get(user_msg_lst[2])[0]
    for col, item in zip([0, 1, 3, 4], user_msg_lst):
        w_sheet.write(new_row, col, item)
    wb.save(file_name)

def all_vip(file_name):
    rb = open_workbook(file_name)
    r_sheet = rb.sheet_by_index(0)
    rows = r_sheet.nrows
    msg = [r_sheet.row_values(row) for row in range(2, rows)]
    return msg

