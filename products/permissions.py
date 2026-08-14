from rest_framework.permissions import BasePermission

class IsAdminReadOnly(BasePermission):
    # Can this user access this view ?
    def has_permission(self, request, view):
        # If the request is a read-only request, allow it for everyone
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # If the request is a other than read-only, then allow it only for authenticated users who are also staff (admin)
        return (
            request.user.is_authenticated
            and request.user.is_staff
        )

# Can this user access this particular product ?
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return obj.owner == request.user