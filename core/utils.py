from rest_framework.viewsets import ModelViewSet


def all_methods(*methods, only_these: bool = False):
    except_methods = methods
    if only_these:
        req_methods = ['put', 'post', 'patch', 'delete', 'get']
        except_methods = list(set(req_methods)-set(methods))

    all_methods = ModelViewSet.http_method_names
    return list(set(all_methods)-set(except_methods))
