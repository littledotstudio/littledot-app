import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io 
import sys
import PyPDF2 as pdf2
from PyPDF2 import PdfReader
import re


def download_pdf(pdf_file):
    try:
        #pdf_file_id = '1qs-aMjQm9iXFVByhm4GyuQTfCYqonjlr'
        pdf_file_id = pdf_file
        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=pdf_file_id)
        #file = io.BytesIO()
        location = '/app/'
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
    reader = PdfReader("tmp.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    new_orders = re.findall(r'Order #(.*?)\n', text, re.DOTALL)
    return new_orders


SCOPES = ['https://www.googleapis.com/auth/drive']
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)


print(creds.valid)
results = service.files().list(pageSize=200, q = "'1avS3yYSwAsG08ylzuo9psJkOihMQfSLV' in parents", fields="nextPageToken, files(id, name)").execute()

# Loops through Laser Jobs folder: https://drive.google.com/drive/u/2/folders/1avS3yYSwAsG08ylzuo9psJkOihMQfSLV
# Looks for something with the name "batch" in it and saves the folder IDs for those guys
new_batch_folder_ids = []
for f in results['files']:
    if "batch" in f['name'].lower():
        new_batch_folder_ids.append(f['id'])

# Loops through the "batch" folders earlier 
# Finds the laser job file, gets the list of orders in that laser job
# Moves corresponding files from the Approved folder: https://drive.google.com/drive/u/2/folders/1XEXTQBX3BlAqFhMSwEARK1jPM07WWdbd
# 
for folder in new_batch_folder_ids:
    new_batch = service.files().list(pageSize=200, q = f"'{folder}' in parents", fields="nextPageToken, files(id, name)").execute()
    for file in new_batch['files']:
        if "laser" in file['name'].lower():
            pdf_file_id = file['id']
            new_orders = download_pdf(pdf_file_id)
            new_orders = [x+".pdf" for x in new_orders]
            moveto_folder = folder
            movefrom_folder = '1XEXTQBX3BlAqFhMSwEARK1jPM07WWdbd'
            approved_folder = service.files().list(pageSize=200, q = f"'{movefrom_folder}' in parents", fields="nextPageToken, files(id, name)").execute()
            for i in range(0, len(approved_folder['files'])):
                file_id = approved_folder['files'][i]['id']
                file_name = approved_folder['files'][i]['name']
                #print(file_name)
                if file_name in new_orders:
                    print("MOVING")
                    print(file_name)
                    file = service.files().update(
                            fileId=file_id,
                            addParents=moveto_folder,
                            removeParents=movefrom_folder,
                            fields='id, parents'
                        ).execute()