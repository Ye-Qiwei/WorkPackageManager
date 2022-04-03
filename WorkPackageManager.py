import openpyxl
import time
import datetime
import PySimpleGUI as sg
import pickle

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
        return data[cw - 1][day - 1]
    else:
        return data

    
class Task:
    def __init__(self, *, name = '', plan_time = 0.0, actual_time = 0.0, comment = '', id = 0):
        self.task_name = name
        self.task_plan_time = plan_time
        self.task_actual_time = actual_time
        self.task_comment = comment
        self.start_time = None
        self.elapsed_time = None
        self.task_id = id

    def read(self):
        return (self.task_name, self.task_plan_time, self.task_actual_time, self.task_comment)

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

    def count_actual_time(self):
        self.start_time = time.time()
        #print('count start')
        return
    
    def update_actual_time(self):
        if self.start_time is not None:
            self.elapsed_time = int(time.time() - self.start_time)
            elapsed_hour = round(self.elapsed_time/3600, 4)
            self.task_actual_time += elapsed_hour
            #print('count time = ' + str(self.task_actual_time) + 'hour')
        return

class DailyInfo:
    def __init__(self, cw = 0, day = 0):
        self.cw = cw
        self.day = day
        self.total_task = []
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)
        datestr = now.strftime('%Y/%m/%d')
        self.txt = datestr + '\n'
    
    def add_task(self,task):
        self.total_task.append(task)
        #print(self.total_task)
        return

    def generate_txt(self):       
        for task_in_list in self.total_task:
            task_txt = str(task_in_list.task_id) + '. ' + task_in_list.task_name + ' (' + str(task_in_list.task_plan_time) + 'h)' + '(✔️' + str(task_in_list.task_actual_time) + 'h)' + ' ' + task_in_list.task_comment + '\n'
            self.txt += task_txt
        return self.txt


def main():
    '''
    task1 = Task(name = 'MTG', comment = 'daily', plan_time = 4.0, id = 1)
    task1.write(actual_time = 2.0)
    task2 = Task(name = 'python programming', plan_time = 2.0, actual_time = 2.0, id = 2)
    task3 = Task(name = 'pc setup', plan_time = 1.0, actual_time = 1.5, id = 3)

    day1 = DailyInfo(day = 1, cw = 1)
    day1.add_task(task1)
    day1.add_task(task2)
    day1.add_task(task3)
    #write_info(cw = day1.cw, day = day1.day, info = day1.generate_txt())

    row, column = (60, 7) 
    database = [[None for i in range(row)] for j in range(column)]
    cw_db = 1
    day_db = 1
    database[cw_db - 1][day_db - 1] = day1
    '''
    
    database = read_database()
    
    
    save_database(database)

''' 
    layout = [[sg.Text(str(day1.total_task[0].task_id) + '. '+ day1.total_task[0].task_name),\
        sg.Text('Plan time: ' + str(day1.total_task[0].task_plan_time) + 'h'),\
            sg.Text('Actual time: ' + str(day1.total_task[0].task_actual_time) + 'h'),\
                sg.Text('Comment: ' + str(day1.total_task[0].task_comment)),\
                    sg.Button('Exit', key = '-exit-')]]

    window = sg.Window('Task Manager ', layout)
    while True:  # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
    window.close()
'''    

if __name__ == "__main__":
    main()