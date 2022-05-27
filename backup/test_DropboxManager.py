import unittest
from DropboxManager import DropboxManager
from vars import DBX_TOKEN

class DropboxTestCase(unittest.TestCase):

    def testUpload(self):
        dbx_manager = DropboxManager(DBX_TOKEN)
        self.assertFalse(dbx_manager.upload_file('test.txt', '/Anteo AI Backup/test.txt'))

        