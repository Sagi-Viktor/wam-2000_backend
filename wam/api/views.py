import json
from io import BytesIO

from django.http import FileResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from services.creation_service import create
from services.download_service import export_file
from services.update_service import update
from services.read_service import get_row_from_table
from services import helper_service as helper
from services.list_spreadsheet_service import list_spreadsheets
from googleapiclient.errors import HttpError
from rest_framework import status

# Imports .env file to read current server host location
import environ

env = environ.Env()
server_location = env("DJANGO_SERVER_HOST_LOCATION")


@api_view(['POST'])
def create_spreadsheet(request):
    """Create Spreadsheet with provided values (title, headers)
    Request Json format:
    {"title": "example-title",
    "headers": {
        "values": [[
                "column-1",
                "column-N",
    ]]}}"""

    try:
        body = json.loads(request.body)
        title = body["title"] if body else "dummy-title"
        headers = body["headers"] if "headers" in body else None
        details = create(title=title,
                         table_header=headers,
                         range_name=helper.calc_range(),
                         value_input_option=helper.USER_ENTERED)
        response = {
            "spreadsheet-title": details["spreadsheet-name"],
            "spreadsheet-id": details["spreadsheet-id"],
            "location-for-headers": f'{server_location}/get?id={details["spreadsheet-id"]}',
            "location-for-download": f'{server_location}/download-raw?id={details["spreadsheet-id"]}',
            "table-header": details["table-header"]["values"][0] if details["table-header"] is not None else None
        }
        return Response(response, status=status.HTTP_201_CREATED)
    except json.decoder.JSONDecodeError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except HttpError:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def update_spreadsheet(request):
    """Update Spreadsheet with provided values (spreadsheet ID, columns)
    Request Json format:
    {"spreadsheet_id": ID,
    "data": {
        "values": [[
                "column-1",
                "column-N",
    ]]}}"""

    try:
        body = json.loads(request.body)
        spreadsheet_id = body["spreadsheet_id"]
        data = body["data"]
        details = update(spreadsheet_id=spreadsheet_id,
                         data=data, range_=helper.calc_range(),
                         value_input_option=helper.USER_ENTERED,
                         insert_data_option=helper.INSERT_ROWS)
        response = {
            "spreadsheet-id": details["spreadsheet-id"],
            "location-for-headers": f'{server_location}/get?id={details["spreadsheet-id"]}',
            "location-for-download": f'{server_location}/download-raw?id={details["spreadsheet-id"]}',
            "data-insertion-direction": details["data-insertion-direction"],
            "table-range": details['table-range'],
            "update-range": details["update-range"],
            "updated-rows": details["updated-rows"],
            "updated-cells": details["updated-cells"],
        }
        return Response(response, status=status.HTTP_201_CREATED)
    except json.decoder.JSONDecodeError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except HttpError:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
def get_headers_from_table(request):
    """Read spreadsheet header if the id provided in a query parameter
    query param: ?id"""

    try:
        spreadsheet_id = request.GET.get('id', False)
        if not spreadsheet_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        details = get_row_from_table(spreadsheet_id=spreadsheet_id,
                                     range_=helper.calc_range(),
                                     value_render_option=helper.VRO_FORMATTED_VALUE,
                                     date_time_render_option=helper.DATE_FORMATTED_STRING)
        response = {
            "spreadsheet-id": spreadsheet_id,
            "location-for-headers": f'{server_location}/get?id={spreadsheet_id}',
            "location-for-download": f'{server_location}/download-raw?id={spreadsheet_id}',
            "major-direction": details["majorDimension"],
            "table-header": details["values"][0] if 'values' in details else None
        }
        return Response(response)
    except HttpError:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
def get_spreadsheets_id(request):
    """Returns a list of spreadsheets IDs and their names
    in descending order based on creation time (The Newest First)"""
    try:
        return Response(list_spreadsheets(), status=status.HTTP_200_OK)
    except HttpError:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['GET'])
def download_spreadsheet(request):
    """Returns a FileResponse() which is a Spreadsheet type file,
    which can be converted and donwloaded in the frontend """
    try:
        spreadsheet_id = request.GET.get('id', False)
        if not spreadsheet_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        spreadsheet_file = export_file(spreadsheet_id)
        # create a file like buffer to receive PDF data.
        buffer = BytesIO()
        buffer.write(spreadsheet_file)
        buffer.seek(0)
        return FileResponse(buffer)
    except HttpError:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
