from __future__ import print_function

from wam.authentication import authentication
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create(title):
    """
    Creates the empty Sheet with given name to the root directory.
    """
    creds = authentication.start()
    try:
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
        return spreadsheet.get('spreadsheetId')
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    create("TestSpreadsheet")
