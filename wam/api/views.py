import json

from rest_framework.response import Response
from rest_framework.decorators import api_view
from services.creation_service import create
from services.update_service import update
from services.helper_service import USER_ENTERED
from services.helper_service import calc_range
from googleapiclient.errors import HttpError
from rest_framework import status


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
        headers = body["headers"] if body["headers"] else None
        return Response(create(title=title,
                               body=headers,
                               range_name=calc_range(),
                               value_input_option=USER_ENTERED), status=status.HTTP_201_CREATED)
    except json.decoder.JSONDecodeError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except HttpError:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def update_spreadsheet(request):

    try:
        body = json.loads(request.body)
        spreadsheet_id = body["spreadsheet_id"]
        data = body["data"]
        return Response(update(spreadsheet_id=spreadsheet_id,
                               data=data, range_=calc_range(),
                               value_input_option=USER_ENTERED,
                               insert_data_option='INSERT_ROWS'), status=status.HTTP_201_CREATED)
    except json.decoder.JSONDecodeError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except HttpError:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
