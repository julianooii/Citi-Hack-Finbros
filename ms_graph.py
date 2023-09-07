import msal
import webbrowser
from msal import PublicClientApplication
import requests
import os

tenent_id = "55dd5550-5d6b-43fd-99c3-caa837fa27dc"
APPLICATION_ID = "27f17a4b-5e7e-477e-866f-6eff3e3aa049"
CLIENT_SECRET = "Bx~8Q~lpYniXgL6vuD56dxLR4UDRAxZ5ZGLpMcua"

base_url = "https://graph.microsoft.com/v1.0/"
authority_url = 'https://login.microsoft.com/consumers/'
scopes = ['Files.Read', 'Files.Read.All']

fileDicts= {}

app = msal.PublicClientApplication(
    APPLICATION_ID,
)
flow = app.initiate_device_flow(scopes=scopes)
print(flow['message'])

webbrowser.open(flow['verification_uri'])
result = app.acquire_token_by_device_flow(flow)
access_token_id = result["access_token"]

folder_dir = input("Enter folder path relative to root folder: ")

headers = {"Authorization" : "Bearer " + access_token_id}

# Get all file details in folder
response_file_info = requests.get(
    base_url + f"/me/drive/root:/{folder_dir}:/children",
    headers=headers
)
list_file_response = response_file_info.json()["value"]

# Map all file id to file name
for fileDetails in list_file_response:
    print(fileDetails["id"])
    fileDicts[fileDetails["id"]] = fileDetails["name"]

# Import all files into tempResources folder using their file name
for fileId in fileDicts:
    response_file_content = requests.get(base_url + f"/me/drive/items/{fileId}/content", 
        headers=headers
    )
    with open(os.path.join(f"{os.getcwd()}/backend/tempResources", fileDicts[fileId]), "wb") as f:
        f.write(response_file_content.content)

    
