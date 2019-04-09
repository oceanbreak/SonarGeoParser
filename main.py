from geoparse import *
from tkinter import *
from tkinter import filedialog, messagebox
from os import getcwd
import os.path

class SonarGeoParser(Frame):

    def __init__(self):
        self.root = Tk()
        Frame.__init__(self)

        self.cur_dir = getcwd()
        self.save_dir = getcwd()

        self.file_list = []
        self.save_file_list = []

        self.coord_buffer = []

        self.root.geometry('500x100')
        self.master.title('Sonar Geo Parser')
        self.createWidgets()
        self.root.mainloop()


    def readfile(self):
        self.file_list = list(filedialog.askopenfilenames(title='Open coordinate files', initialdir = self.cur_dir))
        if self.file_list:
            self.cur_dir = os.path.split(self.file_list[0])[0]
            success_files_number = 0
            values_to_remove = []
            for i, file in enumerate(self.file_list):
                try:
                    cur_array = georead(file)
                    cur_array = getCoordinatesDeg(cur_array)
                    self.coord_buffer.append(cur_array)
                    success_files_number += 1
                except ValueError:
                    cur_array = None
                    values_to_remove.append(file)
                    pass

            self.file_list = [item for item in self.file_list if item not in values_to_remove]
            if values_to_remove:
                messagebox.showerror('Error occured', 'Bad format files:\n%s' % '\n'.join(values_to_remove))
            # messagebox.showinfo('Info', '%i files read successfully: \n%s' % (success_files_number,
            #                                                                   '\n'.join(self.file_list)))
            # print(self.file_list)

    def save_files(self):
        self.save_dir = filedialog.askdirectory(initialdir = self.save_dir)
        for i, cur_array in enumerate(self.coord_buffer):
            fname = os.path.split(self.file_list[i])[1]
            fname = fname.split('.')[0] + '.csv'
            save_file = os.path.join(self.save_dir, fname)
            geosave(cur_array, save_file)
        messagebox.showinfo('Info', '%i files saved successfully in: %s' % (i+1, self.save_dir))


    def createWidgets(self):
        #Configuration var
        labelfont = ('arial', 20)
        label_bg = 'white'
        label_fg = 'black'
        buttonfont = ('arial', 15, 'bold')
        padding_y = 5
        padding_x = 20

        # Buttons and text set
        self.buttons = Frame()
        self.buttons.pack(side=TOP, expand=YES, fill=BOTH, pady=padding_y, padx = padding_x)

        # Buttons
        self.open_button = Button(self.buttons)
        self.open_button['text'] = 'Open'
        self.open_button['command'] = self.readfile

        self.save_button = Button(self.buttons)
        self.save_button['text'] = 'Save'
        self.save_button['command'] = self.save_files


        # Entries

        # Grid elements
        self.open_button.grid(row=0, column=0, pady=padding_y)
        self.save_button.grid(row=1, column=0, pady=padding_y)

app = SonarGeoParser()