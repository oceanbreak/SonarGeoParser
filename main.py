from geoparse import *
from tkinter import *
from tkinter import filedialog, messagebox
from os import getcwd

class SonarGeoParser(Frame):

    def readfile(self):
        file_list = filedialog.askopenfilenames(title='Open coordinate files', initialdir = self.cur_dir)
        i = 0
        for file in file_list:
            new_file = '.'.join(file.split('.')[:-1]) + '.csv'
            try:
                cur_array = georead(file)
                cur_array = getCoordinatesDeg(cur_array)
                geosave(cur_array, new_file)
                i += 1
            except Exception:
                messagebox.showerror('Error occured' , file.split('/')[-1] + ': bad file format')
        messagebox.showinfo('Operation Done', '%i CSV files created successfully' % i)


    def __init__(self):
        self.root = Tk()
        Frame.__init__(self)
        self.cur_dir = getcwd()
        self.root.geometry('500x100')
        self.master.title('Sonar Geo Parser')
        # self.root.mainloop()

app = SonarGeoParser()
app.readfile()
app.destroy()