import datetime
import os
import constants
import shutil

def cleanBackupFolder():
    files = os.listdir(constants.BACKUP_FOLDER_PATH)
    for file in files:
        filePath = os.path.join(constants.BACKUP_FOLDER_PATH, file)
        ti_m = os.path.getmtime(filePath)
        m_datestamp = datetime.date.fromtimestamp(ti_m)
        today = datetime.date.today()
        aMonthAgo = today - datetime.timedelta(days=30)

        if m_datestamp < aMonthAgo:
            os.remove(filePath)

def saveFileToBackupFolder():
    files = os.listdir(constants.OUTPUT_FOLDER_PATH)
    for file in files:
        if file == '.DS_Store':
            continue
        now = str(datetime.datetime.now())[:19]
        now = now.replace(":", "_")
        now = now.replace(" ", "_")
        filePath = os.path.join(constants.OUTPUT_FOLDER_PATH, file)
        fileName = os.path.splitext(file)[0]
        fileExt = os.path.splitext(file)[1]
        target = os.path.join(constants.BACKUP_FOLDER_PATH, f"{fileName}{now}{fileExt}")
        shutil.copyfile(filePath, target)
    return