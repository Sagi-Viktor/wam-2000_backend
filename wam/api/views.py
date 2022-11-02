
from rest_framework.response import Response
from rest_framework.decorators import api_view

from services.creation_service import create


@api_view(['POST'])
def create_spreadsheet(request):
    title = "test_sheet"
    return Response(create(title=title))
