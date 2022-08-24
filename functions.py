import os
import datetime
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
            elif param[0] == "max amount of backups - ":
                max_amount_of_folders = param[1]

        return [save_file_location, time_between_backups, max_amount_of_folders]


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


def update_settings(save_file_location, time_between_backups, max_amount_of_saves):
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
            elif param[0] == "max amount of backups - ":
                settings += "max amount of backups - \"" + max_amount_of_saves + "\"\n"
            else:
                settings += line

    with open("settings.ini", "w") as settings_file:
        settings_file.write(settings)


def delete_oldest_save(max_amount_of_folders):
    """
    Check if there are more than x backups in the backup saves folder. If there are, delete the oldest one.
    If the max amount of backups is 0 or lower, don't delete any backups.
    """

    if max_amount_of_folders <= 0:
        return

    # Get the list of all the folders in the backup saves folder
    files = os.listdir('./backup saves')

    if len(files) > max_amount_of_folders:
        # Sort files by date and time
        files.sort(key=lambda x: os.path.getmtime('./backup saves/' + x))

        oldest_file = files[0]

        # Delete the oldest file
        shutil.rmtree('backup saves/' + oldest_file)

        # Call this function until the amount of folders is less than x (recursion)
        if len(files) > max_amount_of_folders:
            delete_oldest_save(max_amount_of_folders)
