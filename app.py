from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
import time
import os
import functions

# * Get user settings
user_settings = functions.get_user_settings()

# * Global Variables
# Colors
FIRST_COLOR = '#ffffff'
SECOND_COLOR = '#006699'
THIRD_COLOR = '#b7e5ed'
FOURTH_COLOR = '#90dbe8'
FIFTH_COLOR = '#ff0004'
# Default time value in minutes
DEFAULT_TIME_VALUE = user_settings[1]
# Backup Loop Variable
CONTINUE_BACKUP = False
# Default path for the save file
SOURCE_FILE_LOCATION = user_settings[0]
# Max amount of saves stored
MAX_SAVES = user_settings[2]


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

    # Check if the save file exists
    global SOURCE_FILE_LOCATION
    if not functions.verify_if_save_file_exists(SOURCE_FILE_LOCATION):
        messagebox.showerror("File Not Found", "The save file was not found.")
        return

    # Disable backup button and input time field
    backup_button.config(state=DISABLED)
    time_input.config(state=DISABLED)
    stop_button.config(state=NORMAL)

    # update global variable
    global DEFAULT_TIME_VALUE
    DEFAULT_TIME_VALUE = int(input_time_value)

    SOURCE_FILE_LOCATION = save_file_location_input.get()

    global MAX_SAVES
    MAX_SAVES = int(max_saves_input.get())

    # update config file
    functions.update_settings(SOURCE_FILE_LOCATION, str(
        DEFAULT_TIME_VALUE), str(MAX_SAVES))

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
    functions.copy_save_file(SOURCE_FILE_LOCATION)

    # Check for number of saves and delete oldest save if necessary
    functions.delete_oldest_save(MAX_SAVES)

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


def search_path():
    file = filedialog.askopenfile(
        mode='r', filetypes=[('Elden Ring Save File', '*.sl2')])
    if file:
        filepath = os.path.abspath(file.name)

        # Update save_file_location input
        save_file_location_input.delete(0, END)
        save_file_location_input.insert(0, str(filepath))

        # Update global variable
        global SOURCE_FILE_LOCATION
        SOURCE_FILE_LOCATION = str(filepath)

        global DEFAULT_TIME_VALUE
        DEFAULT_TIME_VALUE = time_input.get()

        global MAX_SAVES
        MAX_SAVES = max_saves_input.get()

        # TODO: Update user settings
        functions.update_settings(
            SOURCE_FILE_LOCATION, str(DEFAULT_TIME_VALUE), str(MAX_SAVES))


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
app_title = Label(section, text='Elden Ring - Backup Save', font=(
    "Arial", 22, "bold"), fg=SECOND_COLOR, bg=THIRD_COLOR)
app_title.place(relx=0.50, rely=0.1, anchor="center")

# Save File Location
save_file_location_lbl = Label(section, text="Save File Location:", font=(
    "Arial", 11, "bold"), fg=SECOND_COLOR, bg=THIRD_COLOR)
save_file_location_lbl.place(relx=0.50, rely=0.25, anchor="center")

save_file_location_input = Entry(section, width=45, font=(
    "Arial", 9, "bold"), fg=SECOND_COLOR, bg=THIRD_COLOR, justify=CENTER)
save_file_location_input.place(relx=0.47, rely=0.33, anchor="center")

# Insert default path from the settings file
save_file_location_input.insert(0, SOURCE_FILE_LOCATION)

# Browse Button
browse_button = Button(section, text="Browse", font=(
    "Arial", 7, "bold"), fg=SECOND_COLOR, bg=THIRD_COLOR, relief=GROOVE, command=search_path)
browse_button.place(relx=0.84, rely=0.33, anchor="center")


# Time between backups
time_lbl = Label(section, text='Time between backups:\n(in minutes)', font=(
    "Arial", 11, "bold"), fg=SECOND_COLOR, bg=THIRD_COLOR)
time_lbl.place(relx=0.30, rely=0.5, anchor="center")

# Time input
time_input = Entry(section, width=10, font=(
    "Arial", 11, "bold"), fg=SECOND_COLOR, bg=THIRD_COLOR, justify=CENTER)
time_input.place(relx=0.30, rely=0.63, anchor="center")

# set input to default time value
time_input.insert(0, DEFAULT_TIME_VALUE)


# Max amount of backup saves allowed
max_saves_lbl = Label(section, text='Max amount of\nbackup saves allowed:', font=(
    "Arial", 11, "bold"), fg=SECOND_COLOR, bg=THIRD_COLOR)
max_saves_lbl.place(relx=0.70, rely=0.5, anchor="center")

max_saves_input = Entry(section, width=10, font=(
    "Arial", 11, "bold"), fg=SECOND_COLOR, bg=THIRD_COLOR, justify=CENTER)
max_saves_input.place(relx=0.70, rely=0.63, anchor="center")

# set input to default max saves value
max_saves_input.insert(0, MAX_SAVES)


# Buttons Section
buttons_section = PanedWindow(section, width=340, height=50, bg=FOURTH_COLOR)
buttons_section.place(relx=0.50, rely=0.85, anchor="center")

# Buttons
backup_button = Button(buttons_section, text='Backup', font=("Arial", 14, "bold"), fg=SECOND_COLOR, bg=FOURTH_COLOR, highlightbackground=FIRST_COLOR,
                       highlightcolor=FIRST_COLOR, highlightthickness=1, activebackground=FOURTH_COLOR, activeforeground=SECOND_COLOR, command=backup_save)
backup_button.place(x=0, y=0, width=113, height=50)

stop_button = Button(buttons_section, text='Stop', font=("Arial", 14, "bold"), fg=FIFTH_COLOR, bg=FOURTH_COLOR, highlightbackground=FIRST_COLOR,
                     highlightcolor=FIRST_COLOR, highlightthickness=1, activebackground=FOURTH_COLOR, activeforeground=SECOND_COLOR, state=DISABLED, command=stop_backup_loop)
stop_button.place(x=113, y=0, width=113, height=50)


quit_button = Button(buttons_section, text='Quit', font=("Arial", 14, "bold"), fg=SECOND_COLOR, bg=FOURTH_COLOR, highlightbackground=FIRST_COLOR,
                     highlightcolor=FIRST_COLOR, highlightthickness=1, activebackground=FOURTH_COLOR, activeforeground=SECOND_COLOR, command=lambda: root.destroy())
quit_button.place(x=226, y=0, width=113, height=50)


# Check if the backup folder exists(if not creates one)
functions.check_if_folder_exists()


root.mainloop()
