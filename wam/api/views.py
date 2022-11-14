import json

from rest_framework.response import Response
from rest_framework.decorators import api_view
from services.creation_service import create
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
        try:
            try:
                body = json.loads(request.body)
                title = body["title"] if body else "dummy-title"
                column = body["headers"] if body["headers"] else None
            except json.decoder.JSONDecodeError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(create(title=title, body=column, range_name='A1:C3', value_input_option='USER_ENTERED'), status=status.HTTP_201_CREATED)
    except HttpError:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
