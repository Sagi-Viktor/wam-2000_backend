from __future__ import print_function

import io

from authentication import authentication
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


def export_file(file_id):
    """Download a Document file in PDF format.
    Args:
        file_id : file ID of any workspace document format file
    Returns : IO object with location

    :param file_id:
    """
    creds = authentication.start()

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        # pylint: disable=maybe-no-member
        request = service.files().export_media(fileId=file_id,
                                               mimeType="application/x-vnd.oasis.opendocument.spreadsheet")
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    print(type(file.getvalue()))
    return file.getvalue()


if __name__ == '__main__':
    export_pdf(real_file_id='1zbp8wAyuImX91Jt9mI-CAX_1TqkBLDEDcr2WeXBbKUY')