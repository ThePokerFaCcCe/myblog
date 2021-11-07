from rest_framework.viewsets import ModelViewSet
from django.db.models.base import Model


def all_methods(*methods, only_these: bool = False):
    except_methods = methods
    if only_these:
        req_methods = ['put', 'post', 'patch', 'delete', 'get']
        except_methods = list(set(req_methods)-set(methods))

    all_methods = ModelViewSet.http_method_names
    return list(set(all_methods)-set(except_methods))


def delete_pic_if_new_exists(instance: Model, validated_data, field_name='picture'):
    if validated_data.get(field_name):
        getattr(instance, field_name).delete()
