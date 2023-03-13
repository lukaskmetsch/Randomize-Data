import random
import shutil
import os


import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

# Command for Anaconda Shell to turn this python File into .exe file: python -m PyInstaller --onefile --noupx Randomize_Data.py
# Change Directory before with cd to path of python file


# ATTENTION: DO NOT USE THIS PROGRAMM MULTIPLE TIMES ON THE SAME DATA SET! THE KEY FILE WILL BE OVERRITTEN!


# Attention: Both folders MUST exist before you start
# Attention: The folder to copy your blinded files should contain no other files

# Run by clicking the green arrow in the top right corner
    # The Key File will be in your copied folder. It will let you trace back your blinded files


def directory_walk(path_of_the_directory, path_to_copy):

    list_index = 0
    for root, dirs, files in os.walk(path_of_the_directory): # goes through every folder in directory and list all files in a folder

        if len(dirs) != 0: # if folder is not empty

            ordered_list = list(range(1, len(dirs) + 1)) # creates a list with number entries for all folders
            ranomized_list = random.sample(ordered_list, len(ordered_list)) # shuffles list


        for name in files: # goes through every file

            name_without_numbers = ''.join([i for i in name if not i.isdigit()]) # delets all numbers from string
            file_directory = os.path.join(root, name)  # gives back path of Data

            path_to_copy_subfolder = path_to_copy.split(os.sep) # splits up new path
            path_to_copy_subfolder.append("{}".format(ranomized_list[list_index])) # appends randomized number to path
                                                                                # thereby creates subfolder
            path_to_copy_subfolder = os.path.join(*path_to_copy_subfolder) # joins path together

            if not os.path.exists(path_to_copy_subfolder):
                os.makedirs(path_to_copy_subfolder)  # If folder doesn't exist, it will be created

            shutil.copy2(file_directory, path_to_copy_subfolder)  # copies files from old path to new one

            if name == files[-1]:
                list_index +=1  # if the last file in the folder is reached, the index for the folder to copy in is increased

            ### renaming files ###

            os.rename(os.path.join(path_to_copy_subfolder, name), os.path.join(path_to_copy_subfolder, ''.join([name_without_numbers]))) # removes numbers from file names in new directory

        if len(dirs) != 0:
            Key_file = pd.DataFrame({'Number': ranomized_list, 'Original name': dirs}) # creats Key File as a Dataframe
            Key_file = Key_file.sort_values(by=['Number', 'Original name']) # sorts Key File
            Key_file.to_excel(path_to_copy + "\ " + "Key file.xlsx", index=False)  # saves Key File



### Execution ###

window = tk.Tk()
window.config(bg='#000000')
window.withdraw() # Prevents an empty tkinter window from popping up
Input_Dir = filedialog.askdirectory(parent = window, title = "Choose path for randomizing data") # User can choose Input directory
Output_Dir = filedialog.askdirectory(parent = window, title = "Choose output path for randomized data") # User can choose Output directory

def exectution():
    if not os.listdir(Output_Dir): # checks if output directroy is empty
        directory_walk(Input_Dir, Output_Dir)
        window.quit()

    else:
        win = tk.Tk()
        #win.withdraw()
        #top = Toplevel(win)
        win.geometry("300x150")
        win.title("Error")
        #Label(win, text="Output folder is not empty", font=('Helvetica 14 bold')).pack(pady=20)
        # Create a button
        ttk.Button(win,
                  text='Output folder not Empty. Press to quit', command=win.quit).place(x=50, y=60)
        win.mainloop()

exectution()





