import openpyxl
import time
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

class Task:
    def __init__(self, *, name = '', plan_time = 0.0, actual_time = 0.0, comment = ''):
        self.task_name = name
        self.task_plan_time = plan_time
        self.task_actual_time = actual_time
        self.task_comment = comment
        self.start_time = None
        self.elapsed_time = None

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
    
    def add_task(self,task_info):
        self.total_task.append(task_info)
        #print(self.total_task)
        return

    def generate_txt(self):
        count = 1
        for task_in_list in self.total_task:
            task_txt = str(count) + '. ' + task_in_list[0] + ' (' + str(task_in_list[1]) + 'h)' + '(✔️' + str(task_in_list[2]) + 'h)' + ' ' + task_in_list[3] + '\n'
            self.txt += task_txt
            count += 1
        return self.txt


def main():
    task1 = Task(name = 'mtg', comment = 'daily', plan_time = 4.0)
    task1.write(actual_time = 2.0)

    task2 = Task(name = 'programming', plan_time = 2.0, actual_time = 2.0)
    task3 = Task(name = 'pc setup', plan_time = 1.0, actual_time = 1.5)

    day1 = DailyInfo(day = 1, cw = 1)
    day1.add_task(task1.read())
    day1.add_task(task2.read())
    day1.add_task(task3.read())
    write_info(cw = day1.cw, day = day1.day, info = day1.generate_txt())


    '''
    print(task1.read())
    while True:
        key = input('wait input\n')
        if key == 's':
            task1.count_actual_time()

        if key == 'o':
            task1.update_actual_time()
        
        if key == 'q':
            break
    '''



if __name__ == "__main__":
    main()