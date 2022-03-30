import openpyxl

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

class task:
    task_name = ''
    task_plan_time = 0
    task_actual_time = 0
    task_comment = ''

    def __init__(self, *, name = '', plan_time = 0, actual_time = 0, comment = ''):
        self.task_name = name
        self.task_plan_time = plan_time
        self.task_actual_time = actual_time
        self.task_comment = comment

    def read(self):
        return self.task_name, self.task_plan_time, self.task_actual_time, self.task_comment

    def write(self, name = None, plan_time = None, actual_time = None, comment = None):
        if name is not None:
            self.task_name = name
        if plan_time is not None:
            self.task_plan_time = plan_time
        if actual_time is not None:
            self.task_actual_time = actual_time
        if comment is not None:
            self.task_comment = comment
        return

def main():
    #write_info(2,1,'task')
    #print(read_info(3, 1))
    task1 = task(name = 'mtg', actual_time = 2, comment = 'none', plan_time = 1)
    print(task1.read())
    task1.write(actual_time = 4)
    print(task1.read())


if __name__ == "__main__":
    main()

""""
１．FSF weekly MTG(1h)(✓1h)\n
２．週報(2h)(✓2h)\n
３．VSP関連(2h)(✓1h)\n
４．最終発表資料作成(4.5h)(✓4.5h)\n
"""
"""
# ブック、シートを開く
wb = openpyxl.load_workbook('work.xlsx')
ws = wb.active

task1 = 'FSF weekly MTG'
task1_plan = 1
task1_record = 1
task2 = '週報'
task3 = 'VSP関連'
task4 = '最終発表資料作成'
# セルに書き込み
ws['C2'].value = \
    '１．' + task1 + '(1h)(✓1h)\n' \
        + '２．'+ task2 + '(2h)(✓2h)\n' \
            + '３．'+ task3 + '(2h)(✓1h)\n' \
                + '４．'+ task4 + '(4.5h)(✓4.5h)'

ws['B2'].value = ''

# ファイル名を指定してブックを保存
wb.save('worktest.xlsx')

def plan_formatting():
"""