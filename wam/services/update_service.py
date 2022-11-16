from authentication import authentication
from googleapiclient import discovery


def update(spreadsheet_id, data, range_, value_input_option, insert_data_option):
    """Updates the sheet which has the specified sheet ID
    with the data provided
    :return Dict response"""

    creds = authentication.start()
    service = discovery.build('sheets', 'v4', credentials=creds)
    print(f"Updating Spreadsheet, ID: {spreadsheet_id}")
    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id,
                                                     range=range_, valueInputOption=value_input_option,
                                                     insertDataOption=insert_data_option,
                                                     body=data)
    response = request.execute()
    print(f"{response['updates']['updatedColumns']} cells updated.")
    return response
