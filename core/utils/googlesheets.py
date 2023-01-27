import datetime
import locale

import pygsheets
import calendar


def authorize_client():
    """Open the spreadsheet"""
    client = pygsheets.authorize(service_account_file=r'C:\python_projects\clean_arend_bot\creds.json')
    sh = client.open_by_url('https://docs.google.com/spreadsheets/d/1omnWbZPTKH-9HLz3YfqnBI4YVuzG1YV3el2S1lfztfw')
    return sh


def create_new_sheet(name):
    wks = authorize_client().add_worksheet(name, rows=400, cols=7)
    wks.update_row(index=1, values=['Дата', 'ID', 'Имя', 'Адрес', 'Телефон', 'Время', 'Комментарий'])
    # wks.apply_format(ranges='A1:G1', format_info={'backgroundColor': {'red': 1}})
    wks.apply_format(ranges='A1:G1', format_info={'textFormat': {'bold': True}})


def show_free_dates(product):
    """Return 7 free dates"""
    today = datetime.date.today().strftime("%d/%m/%Y")
    wks = authorize_client().worksheet_by_title(product)
    cells = wks.get_all_values(returnas='matrix')
    free_dates_lst = []
    for val in cells:
        try:
            int(val[0].split('/')[2])
            if val[0] >= today and (val[1] == '' or val[2] == '' or val[3] == ''):
                free_dates_lst.append(val[0])
                if len(free_dates_lst) == 7:
                    return '\n'.join(free_dates_lst)
        except:
            continue


def get_is_free_date(product, date):
    """Checks the selected date. True if selected date is not free"""
    wks = authorize_client().worksheet_by_title(product)
    cells = [i[0] for i in wks.get_all_values(returnas='matrix') if i[1] and i[2] and i[3]]
    return date in cells


def get_index_row(product, date):
    """Return row index of google sheet for write"""
    wks = authorize_client().worksheet_by_title(product)
    cells = wks.get_all_values(returnas='matrix')
    for ind, val in enumerate(cells):
        try:
            int(val[0].split('/')[2])
            if val[0] == date:
                return ind + 1
        except:
            continue


def open_and_update_vacuums_sheet(product, date, all_info):
    wks = authorize_client().worksheet_by_title(product)
    row_ind = get_index_row(product, date)
    cells = wks.get_values(f'B{row_ind}', f'D{row_ind}', returnas='matrix')
    row_col = {0: 'B', 1: 'C', 2: 'D'}
    cell = ''
    for ind, val in enumerate(cells[0]):
        if val == '':
            cell = f'{row_col[ind]}{row_ind}'
            break
    wks.update_value(cell, all_info)


def open_and_update_sheet(product, date, dialog_id, name, address, phone):
    wks = authorize_client().worksheet_by_title(product)
    wks.update_row(index=get_index_row(product, date), values=[dialog_id, name, address, phone], col_offset=1)
    # wks.update_values('A2:A5', [['name1111'], ['name2111'], ['name3111'], ['name4111']])
    # wks = sh.sheet1
    # Update a single cell.
    # wks.update_value('A1', "Numbers on Stufffffffff")
    # wks.add_conditional_formatting('A1', 'A4', 'NUMBER_BETWEEN', {'backgroundColor': {'red': 1}}, ['1', '5'])
    # wks.update_values('A2:A5', [['name1'], ['name2'], ['name3'], ['name4']])

    # cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    # last_row = len(cells) + 1

