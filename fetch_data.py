import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

bq = bigquery.Client()
table0 = 'hubspot.deal'

deal_table = bigquery.TableReference.from_string(
    'radiant-rookery-274409.'+table0
)

rows = bq.list_rows(
    deal_table,
)
# Upsert logic
df_approved = rows.to_dataframe(
    # Optionally, explicitly request to use the BigQuery Storage API. As of
    # google-cloud-bigquery version 1.26.0 and above, the BigQuery Storage
    # API is used by default.
    create_bqstorage_client=True,
)

stages = ['21063207','decisionmakerboughtin','contractsent']
approved_ids = df_approved[df_approved['deal_pipeline_stage_id'].isin(stages)]['property_dealname'].values
approved_ids2 = [x+'.pdf' for x in approved_ids]
SCOPES = ['https://www.googleapis.com/auth/drive']

# Code 05_CodeTesting
#file_id = '1KGSWoD6rbdbIm-Sl8JBxowKobHq21X0V'


# Move
#results = service.files().list(pageSize=10, q = "'1qn5SRq6-o81djmXqMRJYBt1MIJo_aWdI' in parents", fields="nextPageToken, files(id, name)").execute()

#results = service.files().list(pageSize=10, q="name='02_Pending Customer Review'", fields="nextPageToken, files(id, name)").execute()
#results = service.files().list(pageSize=10, q = "'1XU0nCVjQbFlK6bzRLEtLUXngY0HvbLMn' in parents", fields="nextPageToken, files(id, name)").execute()

# results = service.files().list(pageSize=10, q="name='02_Pending Customer Review'", fields="nextPageToken, files(id, name)").execute()
# results = service.files().list(pageSize=10, q="name='03_Approved For Processing'", fields="nextPageToken, files(id, name)").execute()


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


results = service.files().list(pageSize=200, q = "'1XU0nCVjQbFlK6bzRLEtLUXngY0HvbLMn' in parents", fields="nextPageToken, files(id, name)").execute()
for i in range(0, len(results['files'])):
    file_id = results['files'][i]['id']
    file_name = results['files'][i]['name']
    #print(file_name)
    if file_name in approved_ids2:
        print("MOVING")
        print(file_name)
        file = service.files().update(
                fileId=file_id,
                addParents=moveto_folder,
                removeParents=movefrom_folder,
                fields='id, parents'
            ).execute()