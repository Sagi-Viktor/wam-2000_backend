import json

from rest_framework.response import Response
from rest_framework.decorators import api_view
from services.creation_service import create


@api_view(['POST'])
def create_spreadsheet(request):
    body = request.body
    title = json.loads(body)["title"] if body else "dummy-title"
    return Response(create(title=title))
