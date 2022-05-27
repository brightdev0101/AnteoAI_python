import shutil, logging.config, datetime, dropbox, time, sys, os
from datetime import datetime
from DropboxManager import DropboxManager
from MailManager import MailManager
from vars import DATA_PATH, DB_PATH, DBX_TOKEN


def backup():
    """ A function to backup data folder (trends files + customers custom analysis) & database

        Return:
            data_bckp (string) - Name of zip data archive for DATA_PATH backup
            database_bckp (string) - Name of users database for DB_PATH backup

    """

    m = MailManager()

    try:
        folder = datetime.today().strftime("%d%m%Y")
        data_bckp = folder + "/" + "data" + "_" + datetime.today().strftime("%d%m%Y_%H%M%S")
        database_bckp = folder + "/" + "users" + "_" + datetime.today().strftime("%d%m%Y_%H%M%S") + ".db"

        shutil.make_archive(data_bckp, "zip", DATA_PATH)
        shutil.copy(DB_PATH, database_bckp)

        data_bckp += ".zip"

        res = "[ANTEO AI ROUTINE] BACKUP {} & {} Successful".format(data_bckp, database_bckp)
        
        logging.info(res)
        m.sendBackupUpload(res)

        return data_bckp, database_bckp
                    

    except Exception as e:
        res = "[ANTEO AI ROUTINE] BACKUP Failed - {}".format(e)
        logging.error(res)
        m.sendBackupUpload(res)



def upload(data, database):
    """ A function to upload exported backup trough Dropbox API

        Params:
            data (string) - Name of zip data archive for DATA_PATH upload
            database (string) - Name of users database for DB_PATH upload
    """
    
    m = MailManager()

    try:
        dbx_client = DropboxManager(DBX_TOKEN)

        file_to_one = "/Anteo AI Backup/" + data
        file_to_two = "/Anteo AI Backup/" + database

        dbx_client.upload_file(data, file_to_one)
        dbx_client.upload_file(database, file_to_two)

        res = "[ANTEO AI ROUTINE] UPLOAD {} & {} Successful".format(data, database)

        logging.info(res)
        m.sendBackupUpload(res)


    except Exception as e:
        res = "[ANTEO AI ROUTINE] UPLOAD Failed".format(data, database)
        logging.error(res)
        m.sendBackupUpload(res)

 
if __name__ == "__main__":

    # Log setup
    logging.config.fileConfig("log_config.ini", disable_existing_loggers=False)

    # Store a local backup
    data_backup, db_backup = backup()

    # Wait backup process
    time.sleep(10)

    # Upload backup to Dropbox
    upload(data_backup, db_backup)

