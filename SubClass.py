import time
import datetime

class Task:
    def __init__(self, *, name = '', plan_time = 0.0, actual_time = 0.000, comment = '', id = 0):
        self.task_name = name
        self.task_plan_time = plan_time
        self.task_actual_time = actual_time
        self.task_comment = comment
        self.start_time = None
        self.elapsed_time = None
        self.task_id = id
        self.baseline_actual_time = None

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
        self.baseline_actual_time = self.task_actual_time 
        #print('count start')
        return
    
    def update_actual_time(self):
        if self.start_time is not None:
           
            self.elapsed_time = int(time.time() - self.start_time)
            #print('elapsed: ' + str(self.elapsed_time))
            elapsed_hour = round(self.elapsed_time/3600, 3)
            #print('elapsed: ' + str(elapsed_hour))
            self.task_actual_time = elapsed_hour + self.baseline_actual_time
            self.task_actual_time = round(self.task_actual_time, 3)
            #print('count time = ' + str(self.task_actual_time) + 'hour')
        return
    
    def stop_counting(self):
        self.start_time = None
        

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
        return

    def clear_task(self):
        self.total_task = []
        return

    def generate_txt(self):       
        for task_in_list in self.total_task:
            task_txt = str(task_in_list.task_id) + '. ' + task_in_list.task_name + ' (' + str(task_in_list.task_plan_time) + 'h)' + '(✔️' + str(task_in_list.task_actual_time) + 'h)' + ' ' + task_in_list.task_comment + '\n'
            self.txt += task_txt
        return self.txt