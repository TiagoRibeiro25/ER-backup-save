import os
import datetime
import shutil


def check_if_folder_exists():
    """
    If the folder 'backup saves' doesn't exist, create it
    """

    if not os.path.exists('./backup saves'):
        os.makedirs('./backup saves')


def copy_save_file():
    """
    It copies the save file from the game's folder to a folder with the current date and time.
    """

    # * GET THE SOURCE FILE (file to copy)
    elden_ring_folder = "C:\\Users\\" + \
        os.getlogin() + "\\AppData\\Roaming\\EldenRing"

    for file in os.listdir(elden_ring_folder):
        # check if the folder contains only numbers
        if file.isdigit():
            save_folder = elden_ring_folder + "\\" + file
            break

    source_save_file = save_folder + "\\ER0000.sl2"

    # * CREATE A FOLDER WITH CURRENT DATE AND TIME
    current_date = datetime.datetime.now()
    current_date = current_date.strftime("%d.%m.%Y - %H.%M")

    # * CREATE THE DESTINATION FOLDER
    destination_save_file = "./backup saves/" + current_date + "/"
    if not os.path.exists(destination_save_file):
        os.makedirs(destination_save_file)

    # * COPY THE SOURCE FILE TO THE DESTINATION FOLDER
    shutil.copy(source_save_file, destination_save_file)
