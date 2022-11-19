import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io 
import sys

SCOPES = ['https://www.googleapis.com/auth/drive']
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)


print(creds.valid)
#file = service.files().get(fileId=file_id, fields='parents').execute()

#these are test folders
# moveto_folder = '1qn5SRq6-o81djmXqMRJYBt1MIJo_aWdI'
# movefrom_folder = '1euIIyv0ea7Be0UwSNztkStHF0PqOGA92'

moveto_folder = '1XEXTQBX3BlAqFhMSwEARK1jPM07WWdbd'
movefrom_folder = '1XU0nCVjQbFlK6bzRLEtLUXngY0HvbLMn'


results = service.files().list(pageSize=200, q = "'1avS3yYSwAsG08ylzuo9psJkOihMQfSLV' in parents", fields="nextPageToken, files(id, name)").execute()


for i in range(0, len(results['files'])):
    file_id = results['files'][i]['id']
    file_name = results['files'][i]['name']
    #print(file_name)
    # if file_name in approved_ids2:
    #     print("MOVING")
    #     print(file_name)
    #     file = service.files().update(
    #             fileId=file_id,
    #             addParents=moveto_folder,
    #             removeParents=movefrom_folder,
    #             fields='id, parents'
    #         ).execute
    if len(file_name)==11:
        print(file_name)





results = service.files().list(pageSize=200, q = "'1m6HkdBRVOjSloLdVaGzRRywqSyfjaDxE' in parents", fields="nextPageToken, files(id, name)").execute()

for f in results['files']:
    print(f['name'])
    print(f['id'])



file_id = '1qs-aMjQm9iXFVByhm4GyuQTfCYqonjlr'
request = service.files().export_media(fileId=file_id, mimeType='application/pdf')
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print "Download %d%%." % int(status.progress() * 100)





try:
    pdf_file_id = '1qs-aMjQm9iXFVByhm4GyuQTfCYqonjlr'
    # pylint: disable=maybe-no-member
    request = service.files().get_media(fileId=pdf_file_id)
    #file = io.BytesIO()
    location = '/app/gdrive_scripts/'
    filename = 'tmp.pdf'
    fh = io.FileIO(location + filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request, 1024 * 1024 * 1024)
    done = False
    while done is False:
        try:
            status, done = downloader.next_chunk()
        except:
            fh.close()
            os.remove(location + filename)
            sys.exit(1)
        print(f'\rDownload {int(status.progress() * 100)}%.', end='')
        sys.stdout.flush()
    print('') 
except HttpError as error:
    print(F'An error occurred: {error}')
    file = None



