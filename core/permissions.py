from rest_framework import permissions


class IsOwnerOfItem(permissions.BasePermission):
    def has_object_permission(self, req, view, obj):
        obj_user = obj

        if hasattr(obj, 'user'):
            obj_user = obj.user

        return obj_user == req.user


class IsAdmin(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        # The reason I created this class and I didn't used IsAdminUser:
        # In BasePermission class this function always returns True,
        # so I have to override it to works correct with IsOwnerOfItem
        return self.has_permission(request=request, view=view)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, req, view):
        if req.method in permissions.SAFE_METHODS:
            return True
        if req.user.is_authenticated:
            return (req.user.is_staff or req.user.is_admin)

    def has_object_permission(self, req, view, obj):
        self.has_permission(req, view)


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, req, view):
        if req.user.is_authenticated:
            return req.user.is_admin


class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_author
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
