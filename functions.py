import os
import datetime
from random import seed
import shutil


def get_user_settings():
    with open("settings.ini", "r") as settings_file:
        settings = settings_file.readlines()

        for line in settings:
            param = line.split('"')

            if param[0] == "save file location - ":
                save_file_location = param[1]
            elif param[0] == "time between backups - ":
                time_between_backups = param[1]

        return [save_file_location, time_between_backups]


def check_if_folder_exists():
    """
    If the folder 'backup saves' doesn't exist, create it
    """

    if not os.path.exists('./backup saves'):
        os.makedirs('./backup saves')


def verify_if_save_file_exists(path):
    return os.path.exists(path)


def copy_save_file(source_save_file):
    """
    It copies the save file from the game's folder to a folder with the current date and time.
    """

    # * CREATE A FOLDER WITH CURRENT DATE AND TIME
    current_date = datetime.datetime.now()
    current_date = current_date.strftime("%d.%m.%Y - %H.%M")

    # * CREATE THE DESTINATION FOLDER
    destination_save_file = "./backup saves/" + current_date + "/"
    if not os.path.exists(destination_save_file):
        os.makedirs(destination_save_file)

    # * COPY THE SOURCE FILE TO THE DESTINATION FOLDER
    shutil.copy(source_save_file, destination_save_file)


def update_settings(save_file_location, time_between_backups):
    """
    Update the settings.ini file with the new values
    """

    settings = ""

    with open("settings.ini", "r") as settings_file:

        for line in settings_file:
            param = line.split('"')

            if param[0] == "save file location - ":
                settings += "save file location - \"" + save_file_location + "\"\n"
            elif param[0] == "time between backups - ":
                settings += "time between backups - \"" + time_between_backups + "\"\n"
            else:
                settings += line

    with open("settings.ini", "w") as settings_file:
        settings_file.write(settings)
