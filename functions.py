import openpyxl
import pickle
import datetime

def read_info(cw, day, add = 'Work.xlsx'):
    # ブック、シートを開く
    book = openpyxl.load_workbook(add)
    sheet = book.active
    info = sheet.cell(day+1, cw+1).value
    return info

def write_info(cw, day, info, add = 'Work.xlsx'):
    book = openpyxl.load_workbook(add)
    sheet = book.active
    sheet.cell(day+1, cw+1).value = info
    book.save(add)
    return

def save_database(data, *, pkl_file = 'database.pkl'):
    with open(pkl_file, 'wb') as f:
        pickle.dump(data, f)
    return

def read_database(*, read_all = True, cw = None, day = None, pkl_file = 'database.pkl'):
    with open(pkl_file, 'rb') as f:
        data = pickle.load(f)
    if read_all == False:
        return data[day- 1][cw - 1]
    else:
        return data

def isfloat(txt):
    try:
        float(txt)  
        return True
    except ValueError:
        return False

def get_today():
        date = datetime.date.today()
        week = date.isocalendar()[1]
        day = date.isocalendar()[2]
        return week, day
