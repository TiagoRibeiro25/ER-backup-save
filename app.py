from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
import time
import functions

# * Global Variables
# Colors
FIRST_COLOR = '#ffffff'
SECOND_COLOR = '#006699'
THIRD_COLOR = '#b7e5ed'
FOURTH_COLOR = '#90dbe8'
FIFTH_COLOR = '#ff0004'
# Description
APP_DESCRIPTION = "This program will automatically\n backup your save files to a folder."
# Default time value in minutes
DEFAULT_TIME_VALUE = "30"
# Backup Loop Variable
CONTINUE_BACKUP = False


# * Functions
def backup_save():
    """
    It takes the input time value, checks if it's valid, disables the backup button and input time
    field, converts the input time value to seconds, and starts the time backup
    :return: Nothing is being returned.
    """
    # Get Input Time Value
    input_time_value = time_input.get()

    # Check if the input time value is valid (number)
    if not input_time_value.isdigit() or input_time_value == "" or int(input_time_value) <= 0:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return

    # Disable backup button and input time field
    backup_button.config(state=DISABLED)
    time_input.config(state=DISABLED)
    stop_button.config(state=NORMAL)

    global CONTINUE_BACKUP
    CONTINUE_BACKUP = True

    # Convert input time value to milliseconds
    backup_time = int(input_time_value) * 60000

    # Start the time backup
    loop_backup(backup_time)


def loop_backup(time_milliseconds):
    """
    "While CONTINUE_BACKUP is True, copy the save file and wait time seconds to backup again."

    The CONTINUE_BACKUP variable is a global variable that is set to True at the beginning of the
    program. If the user presses the "Stop" button, the CONTINUE_BACKUP variable is set to False, which
    will stop the loop

    :param time: The time in seconds to wait before backing up again
    """
    global CONTINUE_BACKUP

    # Copy the save file
    functions.copy_save_file()

    # Check if the user pressed the "Stop" button
    if CONTINUE_BACKUP:
        root.after(time_milliseconds, lambda: loop_backup(time_milliseconds))


def stop_backup_loop():
    """ 
    The CONTINUE_BACKUP variable is set to False, which will stop the loop
    """
    global CONTINUE_BACKUP
    CONTINUE_BACKUP = False

    backup_button.config(state=NORMAL)
    time_input.config(state=NORMAL)
    stop_button.config(state=DISABLED)


# * Main Window
root = Tk()
root.geometry('500x300')
root.resizable(0, 0)
root.eval('tk::PlaceWindow . center')
root.configure(background=FIRST_COLOR)
root.title('Elden Ring - Automatic Backup')


# * Section
section = PanedWindow(root, width=460, height=260, bg=THIRD_COLOR)
section.place(x=20, y=20)


# Title
app_title = Label(section, text='Elden Ring - Backup Save',
                  font=("Arial", 22, "bold"), fg=SECOND_COLOR, bg=THIRD_COLOR)
app_title.place(relx=0.50, rely=0.1, anchor="center")

# Description
app_description = Label(section, text=APP_DESCRIPTION,
                        font=("Arial", 11, "bold"), fg=SECOND_COLOR, bg=THIRD_COLOR)
app_description.place(relx=0.50, rely=0.3, anchor="center")

# Time between backups
time_lbl = Label(section, text='Time between backups:\n(in minutes)',
                 font=("Arial", 11, "bold"), fg=SECOND_COLOR, bg=THIRD_COLOR)
time_lbl.place(relx=0.50, rely=0.5, anchor="center")

# Time input
time_input = Entry(section, width=10, font=(
    "Arial", 11, "bold"), fg=SECOND_COLOR, bg=THIRD_COLOR, justify=CENTER)
time_input.place(relx=0.50, rely=0.63, anchor="center")

# set input to default time value
time_input.insert(0, DEFAULT_TIME_VALUE)


# Buttons Section
buttons_section = PanedWindow(section, width=340, height=50, bg=FOURTH_COLOR)
buttons_section.place(relx=0.50, rely=0.85, anchor="center")


# Buttons
backup_button = Button(buttons_section, text='Backup',
                       font=("Arial", 14, "bold"), fg=SECOND_COLOR, bg=FOURTH_COLOR, highlightbackground=FIRST_COLOR, highlightcolor=FIRST_COLOR,
                       highlightthickness=1, activebackground=FOURTH_COLOR, activeforeground=SECOND_COLOR, command=backup_save)
backup_button.place(x=0, y=0, width=113, height=50)

stop_button = Button(buttons_section, text='Stop',
                     font=("Arial", 14, "bold"), fg=FIFTH_COLOR, bg=FOURTH_COLOR, highlightbackground=FIRST_COLOR, highlightcolor=FIRST_COLOR,
                     highlightthickness=1, activebackground=FOURTH_COLOR, activeforeground=SECOND_COLOR, state=DISABLED, command=stop_backup_loop)
stop_button.place(x=113, y=0, width=113, height=50)


quit_button = Button(buttons_section, text='Quit',
                     font=("Arial", 14, "bold"), fg=SECOND_COLOR, bg=FOURTH_COLOR, highlightbackground=FIRST_COLOR, highlightcolor=FIRST_COLOR,
                     highlightthickness=1, activebackground=FOURTH_COLOR, activeforeground=SECOND_COLOR,
                     command=lambda: root.destroy())
quit_button.place(x=226, y=0, width=113, height=50)


# Check if the backup folder exists(if not creates one)
functions.check_if_folder_exists()


root.mainloop()
