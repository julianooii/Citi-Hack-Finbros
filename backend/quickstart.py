from __future__ import print_function
#install this package
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io
import shutil

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.readonly']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    #full link --> https://drive.google.com/drive/folders/1DdXx-CfRzcSCYAjCPQVV29wfxkW_yD1g?usp=drive_link
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(q=f"'1DdXx-CfRzcSCYAjCPQVV29wfxkW_yD1g' in parents",
            pageSize=20, fields="nextPageToken, files(id, name)",).execute()
    items = results.get('files', [])

    for id_url in items:
        file_id = id_url['id']
        results = service.files().get(fileId=file_id).execute()
        name = results['name']
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
       
        
        fh.seek(0)
        # Write the received data to the file
        path = "/Users/alden/Documents/GitHub/Citi-Hack-Finbros/downloaded_files/" + name
        with open(path, 'wb') as f:
            shutil.copyfileobj(fh, f)



if __name__ == '__main__':
    main()