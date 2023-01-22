import datetime
import os
import constants
import shutil


def create_backup_folder():
    if not os.path.exists(constants.BACKUP_FOLDER_PATH):
        os.makedirs(constants.BACKUP_FOLDER_PATH)


def clean_backup_folder():
    files = os.listdir(constants.BACKUP_FOLDER_PATH)
    for file in files:
        file_path = os.path.join(constants.BACKUP_FOLDER_PATH, file)
        ti_m = os.path.getmtime(file_path)
        m_datestamp = datetime.date.fromtimestamp(ti_m)
        today = datetime.date.today()
        a_month_ago = today - datetime.timedelta(days=30)

        if m_datestamp < a_month_ago:
            os.remove(file_path)


def save_file_to_backup_folder():
    files = os.listdir(constants.OUTPUT_FOLDER_PATH)
    for file in files:
        if file == '.DS_Store':
            continue
        now = str(datetime.datetime.now())[:19]
        now = now.replace(":", "_")
        now = now.replace(" ", "_")
        file_path = os.path.join(constants.OUTPUT_FOLDER_PATH, file)
        file_name = os.path.splitext(file)[0]
        file_ext = os.path.splitext(file)[1]
        target = os.path.join(constants.BACKUP_FOLDER_PATH, f"{file_name}{now}{file_ext}")
        shutil.copyfile(file_path, target)
    return
