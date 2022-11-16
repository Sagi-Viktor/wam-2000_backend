from authentication import authentication
from googleapiclient import discovery


def get_row_from_table(spreadsheet_id, range_, value_render_option, date_time_render_option):
    """Get a row of data from the specified sheet
    :return Dict response"""

    cred = authentication.start()
    service = discovery.build('sheets', 'v4', credentials=cred)
    print(f"Updating Spreadsheet, ID: {spreadsheet_id}")
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                  range=range_,
                                                  valueRenderOption=value_render_option,
                                                  dateTimeRenderOption=date_time_render_option)
    response = request.execute()
    print(f"{len(response['values'][0])} cells read by server.")
    return response
