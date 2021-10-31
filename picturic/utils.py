import os
from datetime import datetime
from uuid import uuid4
from .settings import UPLOAD_PATH


def upload_to_path(field, instance, filename):
    now = datetime.now()
    return UPLOAD_PATH.format(

        model_name=instance.__class__.__name__,
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour,
        minute=now.minute,
        uuid=uuid4(),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
    )


def upload_to_path_generic(instance, filename):
    return upload_to_path(None, instance.content_object, filename)
