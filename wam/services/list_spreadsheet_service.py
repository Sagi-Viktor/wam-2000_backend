from authentication import authentication
from googleapiclient import discovery


def list_spreadsheets():
    """Lists the spreadsheets ids & names in descending creation time
    :return List file names and IDs"""
    files = []
    page_token = None
    creds = authentication.start()
    service = discovery.build('drive', 'v3', credentials=creds)

    print("Collecting spreadsheet data from Google ...")
    while True:
        request = service.files().list(q="mimeType='application/vnd.google-apps.spreadsheet'",
                                       orderBy='createdTime desc',
                                       spaces='drive',
                                       fields='nextPageToken, ''files(id, name)',
                                       pageToken=page_token)
        response = request.execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    print(f"{len(files)} file found")
    return files
