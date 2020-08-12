import tkinter as tkr
import time
import subprocess
import os
import signal
import sqlite3
from PIL import Image as img
from PIL import ImageTk as imgtk

#WIDGET NAMES ARE DECLARED WITH CAPITAL LETTERS

class Interface:
    def __init__(self):
        self.interface = tkr.Tk()
        self.setup_window_settings()
        self.update_from_database()
        self.create_widgets()
        self.grid_ready_widgets()
        self.interface.mainloop()


    #slaga snimka v backgrounda
    def set_up_background_image(self):
        load = img.open("background.jpg")
        render = imgtk.PhotoImage(load)
        pic = tkr.Label(self.interface, image=render)
        pic.image = render
        pic.place(x=0,y=0)
    #nastroiki na tkinter windowa
    def setup_window_settings(self):
        self.interface.title('Eyecare')
        self.interface.maxsize(757, 505)
        self.interface.resizable(0,0)
        self.set_up_background_image()
        self.interface.iconbitmap('eye.ico')
        #self.interface.attributes('-alpha',1) 
        #self.interface.iconify() a e tova
        #self.interface.overrideredirect(0) -

        
    #writes everything to the database, destroys ALL widgets and createss new ones
    def update_all(self):
        self.write_settings_to_database()
        self.destroy_widgets()
        self.create_widgets()
        self.grid_ready_widgets()
        self.interface.update()
    #writes all swttings to the database, destroys all message widgets and creates new ones
    def update_message(self):
        self.write_settings_to_database()
        self.destroy_message_widgets()
        self.create_text_widgets()
        self.grid_message_widgets()
    #writes all swttings to the database, destroys all time between reminder widgets and creates new ones
    def update_time_between_reminders(self):
        self.write_settings_to_database()
        self.destroy_time_between_reminders_widgets()
        self.create_time_between_reminders_widgets()
        self.grid_time_between_reminders_widgets()
    #writes all swttings to the database, destroys all reminder time on screen widgets and creates new ones
    def update_reminder_time_on_screen_widgets(self):
        self.write_settings_to_database()
        self.destroy_reminder_time_on_screen_widgets()
        self.create_reminder_time_on_screen_widgets()
        self.grid_reminder_time_on_screen_widgets()
    #writes all swttings to the database, destroys all transparency widgets and creates new ones
    def update_transparency_widgets(self):
        self.write_settings_to_database()
        self.destory_transparency_widgets()
        self.create_transparency_widgets()
        self.grid_transparencty_widgets()
    #writes all swttings to the database, destroys all proces status widgets and creates new ones
    def update_process_status_widgets(self):
        self.write_settings_to_database()        
        self.destroy_status_widgets()
        self.create_process_status_widgets()
        self.grid_process_status_widgets()

    #on click functions execute when the "Save" button is pressed and correspond to the right settings
    def on_click_message(self, new_msg):
        self.change_message(new_msg)
        self.update_message()
    def on_click_time_between_reminders(self, new_time_between_reminders):
        self.change_time_between_reminders(int(new_time_between_reminders))
        self.update_time_between_reminders() 
    def on_click_reminder_time_on_screen(self, new_reminder_time_on_screen):
        self.change_reminder_time_on_screen(int(new_reminder_time_on_screen))
        self.update_reminder_time_on_screen_widgets()  
    def on_click_transparency(self, new_transparency):
        self.change_transparency(float(new_transparency))
        self.update_transparency_widgets()
    def on_click_process_status(self):
        if(self.process_status == False):
            self.PID = subprocess.Popen('reminderexe.exe')
            self.process_id_in_string = str(self.PID.pid)
            self.process_status = True
        elif(self.process_status == True):
            #self.PID.terminate()
            #self.PID.kill()
            subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=int(self.process_id_in_string)))
            self.process_status = False
            self.process_id_in_string = 'NULL'
        self.update_process_status_widgets()
    def on_click_save_all(self, settings_list):
        i=0
        for item in settings_list:
            i = i + 1
            if(item != ""):
                if(i == 1):
                    self.change_message(str(item))
                if(i == 2):
                    self.change_time_between_reminders(int(item))
                if(i == 3):
                    self.change_reminder_time_on_screen(int(item))
                if(i == 4):
                    self.change_transparency(float(item))                
        self.update_all()


    #creates all widgets and prepares them to be gridded
    def create_widgets(self):
        self.CLOSE_BUTTON = tkr.Button(text = 'close', command = self.exit_main_loop, width = 16, bg='black', fg='white')
        self.create_text_widgets()
        self.create_time_between_reminders_widgets()
        self.create_reminder_time_on_screen_widgets()
        self.create_transparency_widgets()
        self.create_process_status_widgets()
        self.create_save_all_widget()
    #create text widgets
    def create_text_widgets(self):
        self.MESSAGE_CURRENT = tkr.Label(self.interface, text = 'current message is: ' + self.message)
        self.MESSAGE_ENTRY = tkr.Entry(self.interface)
        self.MESSAGE_BUTTON = tkr.Button(self.interface, text='Save', command=lambda: self.on_click_message(self.MESSAGE_ENTRY.get()))
    #create time between reminders widgets
    def create_time_between_reminders_widgets(self):
        self.TIME_BETWEEN_REMINDERS_CURRENT = tkr.Label(self.interface, text = 'current time between reminders is: ' + str(self.time_between_reminders))
        self.TIME_BETWEEN_REMINDERS_ENTRY = tkr.Entry(self.interface)
        self.TIME_BETWEEN_REMINDERS_BUTTON = tkr.Button(self.interface, text='Save', command=lambda: self.on_click_time_between_reminders(self.TIME_BETWEEN_REMINDERS_ENTRY.get()))
    #create reminder time on screen widgets
    def create_reminder_time_on_screen_widgets(self):
        self.REMINDER_TIME_ON_SCREEN_CURRENT = tkr.Label(self.interface, text = 'current time of reminder on screen is: ' + str(self.reminder_time_on_screen))
        self.REMINDER_TIME_ON_SCREEN_ENTRY = tkr.Entry(self.interface)
        self.REMINDER_TIME_ON_SCREEN_BUTTON = tkr.Button(self.interface, text='Save', command=lambda: self.on_click_reminder_time_on_screen(self.REMINDER_TIME_ON_SCREEN_ENTRY.get()))
    #create transparency widgets
    def create_transparency_widgets(self):
        self.TRANSPARENCY_CURRENT = tkr.Label(self.interface, text = 'current transparency is: ' + str(self.transparency))
        self.TRANSPARENCY_ENTRY = tkr.Entry(self.interface)
        self.TRANSPARENCY_BUTTON = tkr.Button(self.interface, text='Save', command=lambda: self.on_click_transparency(self.TRANSPARENCY_ENTRY.get()))
    #create process status widgets
    def create_process_status_widgets(self):
        self.STATUS_CURRENT = tkr.Label(self.interface, text = 'current status of process: ' + self.process_status_to_string())
        if(self.process_status == True):
            self.STATUS_BUTTON = tkr.Button(self.interface, text = 'ON/OFF', command = self.on_click_process_status, bg='green')
        else:
            self.STATUS_BUTTON = tkr.Button(self.interface, text = 'ON/OFF', command = self.on_click_process_status, bg='#8b0000')
    #create "Save all" widget to save all unsaved changes
    def create_save_all_widget(self):
        self.SAVE_ALL = tkr.Button(self.interface, text = 'Save all',height=7, command=lambda: self.on_click_save_all([self.MESSAGE_ENTRY.get(),self.TIME_BETWEEN_REMINDERS_ENTRY.get(),self.REMINDER_TIME_ON_SCREEN_ENTRY.get(),self.TRANSPARENCY_ENTRY.get()]))
                


    #grids all the ready widgets        
    def grid_ready_widgets(self):
        self.grid_message_widgets()
        self.grid_time_between_reminders_widgets()
        self.grid_reminder_time_on_screen_widgets()
        self.grid_transparencty_widgets()
        self.grid_process_status_widgets()
        self.CLOSE_BUTTON.grid(row=6,column=0)
        self.grid_save_all_widget()
    #grids all ready text widgets
    def grid_message_widgets(self):
        self.MESSAGE_CURRENT.grid(row=1, column=0)
        self.MESSAGE_ENTRY.grid(row=1, column=1)
        self.MESSAGE_BUTTON.grid(row=1, column=2)
    #grids all ready time between reminders widgets
    def grid_time_between_reminders_widgets(self):
        self.TIME_BETWEEN_REMINDERS_CURRENT.grid(row=2, column=0)
        self.TIME_BETWEEN_REMINDERS_ENTRY.grid(row=2, column=1)
        self.TIME_BETWEEN_REMINDERS_BUTTON.grid(row=2, column=2)
    #grids all reminder time on screen widgets
    def grid_reminder_time_on_screen_widgets(self):
        self.REMINDER_TIME_ON_SCREEN_CURRENT.grid(row=3, column=0)
        self.REMINDER_TIME_ON_SCREEN_ENTRY.grid(row=3, column=1)
        self.REMINDER_TIME_ON_SCREEN_BUTTON.grid(row=3, column=2)
    #grids all transparency widgets
    def grid_transparencty_widgets(self):
        self.TRANSPARENCY_CURRENT.grid(row=4, column=0)
        self.TRANSPARENCY_ENTRY.grid(row=4, column=1)
        self.TRANSPARENCY_BUTTON.grid(row=4, column=2)
    #grid process status widgets
    def grid_process_status_widgets(self):
        self.STATUS_CURRENT.grid(row=5, column=0)
        self.STATUS_BUTTON.grid(row=5, column=1)
    #grid save all widget
    def grid_save_all_widget(self):
        self.SAVE_ALL.grid(row=1,column=3,rowspan=4)
        #self.SAVE_ALL.pack()

    
    #destroys all widgets in application
    def destroy_widgets(self):
        self.CLOSE_BUTTON.grid_remove()
        self.destroy_message_widgets()
        self.destroy_time_between_reminders_widgets()
        self.destroy_reminder_time_on_screen_widgets()
        self.destory_transparency_widgets()
        self.destroy_status_widgets()
        self.destroy_save_all_widget()
    #destorys the 3 widgets used to operate the text message
    def destroy_message_widgets(self):
        self.MESSAGE_CURRENT.grid_remove()
        self.MESSAGE_ENTRY.grid_remove()
        self.MESSAGE_BUTTON.grid_remove()
    #destroys the 3 widgets used to operate the working time
    def destroy_time_between_reminders_widgets(self):
        self.TIME_BETWEEN_REMINDERS_CURRENT.grid_remove()
        self.TIME_BETWEEN_REMINDERS_ENTRY.grid_remove()
        self.TIME_BETWEEN_REMINDERS_BUTTON.grid_remove()
    #destroys the 3 widgets used to operate time of rest
    def destroy_reminder_time_on_screen_widgets(self):
        self.REMINDER_TIME_ON_SCREEN_CURRENT.grid_remove()
        self.REMINDER_TIME_ON_SCREEN_ENTRY.grid_remove()
        self.REMINDER_TIME_ON_SCREEN_BUTTON.grid_remove()
    #destroys the 3 widgets used to operate transparency of reminder
    def destory_transparency_widgets(self):
        self.TRANSPARENCY_CURRENT.grid_remove()
        self.TRANSPARENCY_ENTRY.grid_remove()
        self.TRANSPARENCY_BUTTON.grid_remove()
    #destroy the 2 widgets used to operate the pocess status
    def destroy_status_widgets(self):
        self.STATUS_CURRENT.grid_remove()
        self.STATUS_BUTTON.grid_remove()
    #destroy save all widget
    def destroy_save_all_widget(self):
        self.SAVE_ALL.grid_remove()

        

    def process_status_to_string(self):
        if(self.process_status == False):
            return 'OFF'
        elif(self.process_status == True):
            return 'ON'
        
    def exit_main_loop(self):
        self.interface.quit()

    def destroy(self):
        self.interface.destroy()

    def change_transparency(self, new_transparency):
        self.transparency = new_transparency

    def change_time_between_reminders(self, new_time_between_reminders):
        self.time_between_reminders = new_time_between_reminders

    def change_reminder_time_on_screen(self, new_reminder_time_on_screen):
        self.reminder_time_on_screen = new_reminder_time_on_screen

    def change_message(self, new_message):
        self.message = new_message


    def update_from_database(self):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        
        cur.execute("SELECT message FROM settings")
        temp = cur.fetchall()
        self.message = temp[0][0]

        cur.execute("SELECT transparency FROM settings")
        temp = cur.fetchall()
        self.transparency = temp[0][0]

        cur.execute("SELECT time_between_reminders FROM settings")
        temp = cur.fetchall()
        self.time_between_reminders = temp[0][0]

        cur.execute("SELECT time_of_reminder_on_screen FROM settings")
        temp = cur.fetchall()
        self.reminder_time_on_screen = temp[0][0]

        cur.execute("SELECT process_status FROM settings")
        temp = cur.fetchall()
        if(temp[0][0] == 1):
            self.process_status = True
        else:
            self.process_status = False

        cur.execute("SELECT PID_STR FROM settings")
        temp = cur.fetchall()
        self.process_id_in_string = temp[0][0]
        
    def write_settings_to_database(self):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        str1 = ''' UPDATE settings 
                    SET message = ?,
                    transparency = ?,
                    time_between_reminders = ?,
                    time_of_reminder_on_screen = ?,
                    process_status = ?,
                    PID_STR = ?'''
        if(self.process_status == False):
            help1 = 0
        elif(self.process_status == True):
            help1 = 1
        help2 = (self.message, self.transparency,
                 self.time_between_reminders, self.reminder_time_on_screen,
                 help1, self.process_id_in_string)
        cur.execute(str1, help2)
        
        conn.commit()
