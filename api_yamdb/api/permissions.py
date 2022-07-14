from rest_framework.permissions import SAFE_METHODS, BasePermission
import unicodedata


def normalize_caseless(text):
    return unicodedata.normalize("NFKD", text.casefold())


def caseless_equal(left, right):
    return normalize_caseless(left) == normalize_caseless(right)


class IsAdmin(BasePermission):
    """
    Allows access only for admins to everything.
    """

    def has_permission(self, request, view):
        return caseless_equal(request.user.role, 'admin')

    def has_object_permission(self, request, view, obj):
        return caseless_equal(request.user.role, 'admin')   


class IsUserOwner(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj  