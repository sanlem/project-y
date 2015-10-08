import uuid
import os
from django.conf import settings


def generate_unique_upload_filename(directory, extension):
    """
    Returns filename for uploading that is not exists yet
    :param directory: directory under MEDIA_ROOT
    :param extension: file extension, e.g. for images .jpg
    :return: absolute path to file
    """
    while True:
        filename = str(uuid.uuid4())
        path = os.path.join(directory, "{}.{}".format(filename, extension))
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, path)):
            return path
