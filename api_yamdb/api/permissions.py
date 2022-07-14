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


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    def has_permissions(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.method == 'POST'
            and request.user.is_authenticated
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
