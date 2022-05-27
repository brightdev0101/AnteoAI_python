import dropbox, sys, os


class DropboxManager:
    """ This class manage Dropbox API endpoints
    """

    def __init__(self, access_token):
        """ Dropbox class constructor

            Attribs:
                access_token (string) - Token for using API in Dropbox app
        """

        self.access_token = access_token


    def upload_file(self, file_from, file_to):
        """ This method use Dropbox upload endpoint

            Params:
                file_from (string) - Local path backup to upload
                file_to (string) - Destination path backup on cloud


            Limit:
                Do not use this to upload a file larger than 150 MB. Instead, create an upload session.
        """

        try:
            dbx = dropbox.Dropbox(self.access_token)
            
            if file_from != None and file_to != None:
                r_file_from = open(file_from, 'rb')
                r_file_from = r_file_from.read()

                dbx.files_upload(r_file_from, file_to)
            

        except Exception as e:
            print("[ANTEO AI ROUTINE] UPLOAD Failed - {}").format(e)


