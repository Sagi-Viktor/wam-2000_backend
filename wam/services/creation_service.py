from __future__ import print_function

from authentication import authentication
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create(title, table_header, range_name, value_input_option):
    """
    Creates the empty Sheet with given name to the root directory.
    """
    creds = authentication.start()
    try:
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = {
            'properties': {
                'title': title
            },
        }
        # creates new spreadsheet
        spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()

        # write headers into the new spreadsheet
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet.get('spreadsheetId'), range=range_name,
            valueInputOption=value_input_option, body=table_header).execute()

        return {
            'spreadsheet-name': title,
            'spreadsheet-id': spreadsheet.get('spreadsheetId'),
            'table-header': table_header,
        }
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    create("TestSpreadsheet")
