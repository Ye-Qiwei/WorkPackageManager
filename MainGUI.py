import PySimpleGUI as sg

import functions
from SubClass import Task
from SubClass import DailyInfo
    
class UserInterfaces:
    def __init__(self,database):
        self.db = database
        sg.theme('SystemDefault')

        self.window_date = None
        self.window_update_task = None
        self.window_task_info = None

        self.chosen_cw = None
        self.chosen_day = None

        self.show_date_gui = True
        self.show_input_task_gui = False
        self.show_task_info_gui = False

    def show_gui(self):
        while True:
            if self.show_date_gui:
                self.date_gui()
            if self.show_input_task_gui:
                self.input_task_gui(self.chosen_cw, self.chosen_day)
            if self.show_task_info_gui:
                self.task_info_gui(self.chosen_cw, self.chosen_day)
            show_gui_all = (self.show_date_gui, self.show_input_task_gui, self.show_task_info_gui)
            if not any(show_gui_all):
                break

    def date_gui(self):
        button1 = sg.Button('Today', key = '-today-', size = (5,1), font=('Arial',12))
        
        week_days = ['Monday', ' Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        combo = sg.Combo(week_days, default_value = 'Choose day of week', size = (20,1), readonly = True, key = '-day-', enable_events = True, font=('Arial',16))

        text = sg.Text('Calendar week: ', font=('Arial',16))
        
        input = sg.InputText(size = (10,1), key='-cw-', font=('Arial',16))

        button2 = sg.Button('Show Tasks', key = '-showtask-', size = (10,1), font=('Arial',12)) 
        
        button3 = sg.Button('Edit', key = '-edit-', size = (5,1), font=('Arial',12))

        layout = [[text, input, combo], [button1], [button2, button3]]
        self.window_date = sg.Window('Task Manager --Welcome', layout)

        today = functions.get_today()
        today_week = today[0]
        today_day = today[1]

        while self.show_date_gui:  # Event Loop
            event, values = self.window_date.read()
            if event == sg.WIN_CLOSED:
                self.show_date_gui = False
                break

            if event == '-today-':
                self.window_date['-day-'].Update(value = week_days[today_day-1])
                self.window_date['-cw-'].Update(value = today_week)

            if event == '-edit-':
                if (values['-day-'] in week_days) and (values['-cw-'].isdigit()) and (1 <= int(values['-cw-']) <= 52):
                    self.chosen_cw = int(values['-cw-'])
                    self.chosen_day = int(week_days.index(values['-day-']) + 1)
                    self.show_date_gui = False
                    self.show_input_task_gui = True
                    break
                else:
                    sg.popup('Wrong Input!', font=('Arial',12))
                    continue
            
            if event == '-showtask-':
                if (values['-day-'] in week_days) and (values['-cw-'].isdigit()) and (1 <= int(values['-cw-']) <= 52):
                    self.chosen_cw = int(values['-cw-'])
                    self.chosen_day = int(week_days.index(values['-day-']) + 1)
                    self.show_date_gui = False
                    self.show_task_info_gui = True
                    break
                else:
                    sg.popup('Wrong Input!', font=('Arial',12))
                    continue
            
        self.window_date.close()
        

    def task_info_gui(self, cw_this = None, day_this = None):
        daily_info = self.db[day_this - 1][cw_this - 1]
        if daily_info != None:
            task_num = len(daily_info.total_task)
            text_top = sg.Text('Task for today: ', font=('Arial',16))
        else:
            task_num = 0
            text_top = sg.Text('Please edit task: ', font=('Arial',16))

        info_row = [[]]

        empty_text = sg.Text('', font=('Arial',12), size = (3,1))
        text_name = sg.Text('Task Name: ', font=('Arial',12), size = (25,1))
        text_plan = sg.Text('Plan/(h): ', font=('Arial',12), size = (8,1))
        text1_actual = sg.Text('Actual/(h): ', font=('Arial',12), size = (8,1))
        text_comment = sg.Text('Comment: ', font=('Arial',12), size = (25,1))
        row0 = [empty_text, text_name, text_plan, text1_actual, text_comment]
        
        button1 = sg.Button('Choose date', key = '-backtodate-', size = (10,1), font=('Arial',12))
        button2 = sg.Button('Edit', key = '-edit-', size = (6,1), font=('Arial',12))

        if task_num != 0:
            for index in range(1,task_num + 1):
                globals()[f'text{index}_0'] = sg.Text(str(daily_info.total_task[index-1].task_id), font=('Arial',12), size = (3,1))
                globals()[f'text{index}_1'] = sg.Text(str(daily_info.total_task[index-1].task_name), font=('Arial',12), size = (25,1))
                globals()[f'text{index}_2'] = sg.Text(str(daily_info.total_task[index-1].task_plan_time), font=('Arial',12), size = (8,1))
                globals()[f'text{index}_3'] = sg.Text(str(daily_info.total_task[index-1].task_actual_time), font=('Arial',12), size = (8,1))
                globals()[f'text{index}_4'] = sg.Text(str(daily_info.total_task[index-1].task_comment), font=('Arial',12), size = (25,1))
                globals()[f'button_start{index}'] = sg.Button('Start', key = f'-start{index}-', size = (6,1), font=('Arial',12))
                globals()[f'button_end{index}'] = sg.Button('End', key = f'-end{index}-', size = (6,1), font=('Arial',12))
                globals()[f'row{index}'] = [globals()[f'text{index}_0'], globals()[f'text{index}_1'], globals()[f'text{index}_2'], globals()[f'text{index}_3'], globals()[f'text{index}_4'], globals()[f'button_start{index}'], globals()[f'button_end{index}']]
                info_row.append(globals()[f'row{index}'])
            layout = [[text_top], [row0], info_row, [button1, button2]]

        else:
            layout = [[text_top], [button1, button2]]
        
        self.window_task_info = sg.Window('Task Manager --Task Info', layout)

        while self.show_task_info_gui:
            event, values = self.window_task_info.read()
            if event == sg.WIN_CLOSED:
                self.show_task_info_gui = False
                break

            if event == '-edit-':
                self.chosen_cw = cw_this
                self.chosen_day = day_this
                self.show_task_info_gui = False
                self.show_input_task_gui = True
                break

            if event == '-backtodate-':
                self.show_date_gui = True
                self.show_task_info_gui = False
                break
                           
        self.window_task_info.close()

    def input_task_gui(self, cw_this = None, day_this = None):
        daily_info = self.db[day_this - 1][cw_this - 1]
        if daily_info != None:
            task_num = len(daily_info.total_task)
        else:
            task_num = 0
        
        total_task = 8

        empty_text = sg.Text('', font=('Arial',12), size = (3,1))
        text_name = sg.Text('Task Name: ', font=('Arial',12), size = (25,1))
        text_plan = sg.Text('Plan/(h): ', font=('Arial',12), size = (8,1))
        text1_actual = sg.Text('Actual/(h): ', font=('Arial',12), size = (8,1))
        text_comment = sg.Text('Comment: ', font=('Arial',12), size = (20,1))
        row0 = [empty_text, text_name, text_plan, text1_actual, text_comment]
        
        for index in range(1,total_task + 1):
            if index <= task_num:
                globals()[f'input{index}_0'] = sg.InputText(default_text = str(daily_info.total_task[index-1].task_id), key=f'-id{index}-', font=('Arial',12), size = (3,1))
                globals()[f'input{index}_1'] = sg.InputText(default_text = str(daily_info.total_task[index-1].task_name), key=f'-name{index}-', font=('Arial',12), size = (25,1))
                globals()[f'input{index}_2'] = sg.InputText(default_text = str(daily_info.total_task[index-1].task_plan_time), key=f'-plantime{index}-', font=('Arial',12), size = (8,1))
                globals()[f'input{index}_3'] = sg.InputText(default_text = str(daily_info.total_task[index-1].task_actual_time), key=f'-actualtime{index}-', font=('Arial',12), size = (8,1))
                globals()[f'input{index}_4'] = sg.InputText(default_text = str(daily_info.total_task[index-1].task_comment), key=f'-comment{index}-', font=('Arial',12), size = (20,1))
                globals()[f'row{index}'] = [globals()[f'input{index}_0'], globals()[f'input{index}_1'], globals()[f'input{index}_2'], globals()[f'input{index}_3'], globals()[f'input{index}_4']]
            else:
                globals()[f'input{index}_0'] = sg.InputText('', key=f'-id{index}-', font=('Arial',12), size = (3,1))
                globals()[f'input{index}_1'] = sg.InputText('',key=f'-name{index}-', font=('Arial',12), size = (25,1))
                globals()[f'input{index}_2'] = sg.InputText('', key=f'-plantime{index}-', font=('Arial',12), size = (8,1))
                globals()[f'input{index}_3'] = sg.InputText('', key=f'-actualtime{index}-', font=('Arial',12), size = (8,1))
                globals()[f'input{index}_4'] = sg.InputText('', key=f'-comment{index}-', font=('Arial',12), size = (20,1))
                globals()[f'row{index}'] = [globals()[f'input{index}_0'], globals()[f'input{index}_1'], globals()[f'input{index}_2'], globals()[f'input{index}_3'], globals()[f'input{index}_4']]
        
        button1 = sg.Button('Update', key = '-update-', size = (6,1), font=('Arial',12))
        button2 = sg.Button('Clear', key = '-clear-', size = (6,1), font=('Arial',12))
        button3 = sg.Button('Choose date', key = '-backtodate-', size = (10,1), font=('Arial',12))
        button4 = sg.Button('Show Tasks', key = '-showtask-', size = (10,1), font=('Arial',12)) 

        layout = [[row0, row1, row2, row3, row4, row5, row6, row7, row8],[button1, button2], [button3, button4]] # type: ignore 
        
        self.window_update_task = sg.Window('Task Manager --Update Task', layout)
        
        while self.show_input_task_gui:  # Event Loop
            event, values = self.window_update_task.read()
            if event == sg.WIN_CLOSED:
                self.show_input_task_gui = False
                break

            if event == '-update-':
                if daily_info != None:
                    daily_info.clear_task()
                else:
                    daily_info = DailyInfo(cw = cw_this, day = day_this)
            
                for index in range(1,total_task + 1):
                    new_name = values[f'-name{index}-']
                    new_id = values[f'-id{index}-']
                    new_plan_time = values[f'-plantime{index}-']
                    new_actual_time = values[f'-actualtime{index}-']
                    new_comment = values[f'-comment{index}-']
                    if (new_name != '') or (new_id != '') and (new_plan_time != '') or (new_actual_time != '') or (new_comment != ''):
                        if new_id == '':
                            new_id = '0'
                        if new_plan_time == '':
                            new_plan_time = '0.0'
                        if new_actual_time == '':
                            new_actual_time = '0.0'
                        if not functions.isfloat(new_plan_time):
                            sg.popup(f'Wrong Plan Time Input! ({new_plan_time})', font=('Arial',12))
                            new_plan_time = '0.0'
                        if not functions.isfloat(new_actual_time):
                            sg.popup(f'Wrong Actual Time Input! ({new_actual_time})', font=('Arial',12))
                            new_actual_time = '0.0'
                            
                        globals()[f'task{index}'] = Task(name = new_name, id = int(new_id), plan_time = float(new_plan_time), actual_time = float(new_actual_time), comment = new_comment)
                        daily_info.add_task(globals()[f'task{index}'])

                self.db[day_this - 1][cw_this - 1] = daily_info
                functions.save_database(self.db)

            if event == '-clear-':
                for index in range(1,total_task + 1):
                    self.window_update_task[f'-name{index}-'].Update(value = '')
                    self.window_update_task[f'-id{index}-'].Update(value = '')
                    self.window_update_task[f'-plantime{index}-'].Update(value = '')
                    self.window_update_task[f'-actualtime{index}-'].Update(value = '')
                    self.window_update_task[f'-comment{index}-'].Update(value = '')
            
            if event == '-backtodate-':
                self.show_date_gui = True
                self.show_input_task_gui = False
                break
            
            if event == '-showtask-':
                self.chosen_cw = cw_this
                self.chosen_day = day_this
                self.show_input_task_gui = False
                self.show_task_info_gui = True
                break

        self.window_update_task.close()   
        
        #print(daily_info.generate_txt())
        return


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
    
    database = functions.read_database()

    ui = UserInterfaces(database)
    ui.show_gui()


    #functions.save_database(database)  

if __name__ == "__main__":
    main()