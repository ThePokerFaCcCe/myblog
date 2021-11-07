"""
I think this is a very bad way to do that but it works :))
"""

import os
from typing import Any, Optional, Tuple
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile, ImageFileDescriptor
from django.conf import settings
from PIL import Image
from .utils import upload_to_path

SEPARATE_STR = '*'


class PictureFileField(ImageFieldFile):
    def __init__(self, committed: bool, image: ImageFieldFile, thumbnail: Optional[ImageFieldFile] = None, _file=None, name=None):
        super().__init__(image.instance, image.field, image.name)
        self.image = image
        self.thumbnail = thumbnail
        self._committed = committed
        self._has_thumbnail = True if thumbnail else False
        self._file = _file
        self.name = name or image.name

    @property
    def has_thumbnail(self) -> bool:
        return self._has_thumbnail

    def delete(self, save=False) -> None:
        try:
            self.image.delete(save=save)
        except:
            pass
        try:
            self.thumbnail.delete(save=save)
        except:
            pass
        setattr(self.instance, self.field.name, None)


class PictureDescriptor(ImageFileDescriptor):
    def _create_file(self, instance, field, path):
        return ImageFieldFile(instance, field, path)

    def __get__(self, instance, cls=None):
        data = super().__get__(instance, cls)
        if isinstance(data, ImageFieldFile):
            # print(data.__dict__)
            text = data.name
            # if not isinstance(text,str):
            #     return data
            if not isinstance(text, str) or SEPARATE_STR not in text:
                return PictureFileField(
                    image=self._create_file(instance, data.field, text),
                    committed=data._committed,
                    _file=data._file,
                    name=data.name
                )

            img, thumb = text.split(SEPARATE_STR, 1)
            return PictureFileField(
                image=self._create_file(instance, data.field, img),
                thumbnail=self._create_file(instance, data.field, thumb),
                committed=data._committed
            )

        return data


class PictureField(ImageField):
    """
    Custom ImageField with thumbnail support

    ---    
    attributes
    ----------
    >>> field
    < PictureFileField ...> 
    >>> field.image
    < ImageFieldFile ...>
    >>> field.thumbnail
    < ImageFieldFile ...> | None
    >>> field.has_thumbnail
    bool

    other `field` attributes are same as `field.image` attributes

    """
    descriptor_class = PictureDescriptor
    _upload_to_path = upload_to_path

    def __init__(self, upload_to='', use_upload_to_func: bool = False, make_thumbnail: bool = False,
                 verbose_name: Optional[str] = None, name: Optional[str] = None,
                 width_field: Optional[str] = None, height_field: Optional[str] = None,
                 thumbnail_size: Tuple[int, int] = (200, 200),
                 **kwargs: Any
                 ) -> None:
        """
        Parameters
        -----------
        use_upload_to_func : bool
            A function that creates path for files.
        """
        self.thumbnail_size, self.make_thumbnail = thumbnail_size, make_thumbnail
        if use_upload_to_func:
            upload_to = self._upload_to_path
        kwargs['max_length'] = 9999
        super().__init__(upload_to=upload_to, verbose_name=verbose_name, name=name, width_field=width_field, height_field=height_field, **kwargs)

    def pre_save(self, model_instance, add):
        #print("[PRE SAVE]  -  ",getattr(model_instance, self.attname).__dict__)
        file = super().pre_save(model_instance, add)
        if self.make_thumbnail and file.name:
            try:
                thumb_path = self._make_thumbnail(file)
            except:
                pass
            else:
                file.name = SEPARATE_STR.join([file.name, thumb_path])
                setattr(model_instance, self.attname, file)
        return file

    def _make_thumbnail(self, image):
        if not image:
            return ''
        img_relpath = os.path.relpath(image.path, settings.BASE_DIR)
        img_dir, img_name = os.path.split(img_relpath)

        thumb_name = f"thumb_{img_name}"
        thumb_path = os.path.join(img_dir, thumb_name)

        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(self.thumbnail_size)
        img.save(thumb_path)

        img_relpath_no_media_root = os.path.relpath(
            image.path, settings.__dict__.get('MEDIA_ROOT', '.')
        )

        img_dir_no_media_root = os.path.split(
            img_relpath_no_media_root
        )[0]

        thumb_path_no_media_root = os.path.join(
            img_dir_no_media_root, thumb_name
        )

        return thumb_path_no_media_root

    def get_prep_value(self, value: Any) -> Any:
        ## print('[PRE] - ', value)
        return super().get_prep_value(value)
