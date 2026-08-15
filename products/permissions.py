from rest_framework.permissions import BasePermission

# class IsAdminReadOnly(BasePermission):
#     # Can this user access this view ?
#     def has_permission(self, request, view):
#         # If the request is a read-only request, allow it for everyone
#         if request.method in ["GET", "HEAD", "OPTIONS"]:
#             return True

#         if request.method == "DELETE":
#             return request.user.is_staff

#         # If the request is a other than read-only, then allow it only for authenticated users who are also staff (admin)
#         return request.user.is_staff

# class ProductPermission(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in ["GET", "HEAD", "OPTIONS"]:
#             return True

#         if request.method == "DELETE":
#             return request.user.is_staff

#         return request.user.is_authenticated

# # Can this user access this particular product ?
# class IsOwnerOrAdmin(BasePermission):

#     def has_permission(self, request, view):
#         return request.user.is_athenticated

#     def has_object_permission(self, request, view, obj):
#         if request.user.is_staff:
#             return True

#         return obj.owner == request.user

# class IsAdminOrManager(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(
#             name__in=["Admin", "Manager"]
#         ).exists()

# class IsUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(
#             name="User"
#         ).exists()

# This is the concept of Role Based Access Control (RBAC)
class ProductRBACPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # Admin can do everything
        if user.groups.filter(name="Admin").exists():
            return True

        if user.groups.filter(name="Manager").exists():

            allowed_actions = [
                "list",
                "retrieve",
                "create",
                "update",
                "partial_update",
                "mark_out_of_stock",
                "low_stock",
            ]

            return view.action in allowed_actions

        # Normal User permissions
        if user.groups.filter(name="User").exists():

            allowed_actions = [
                "list",
                "retrieve",
            ]

            return view.action in allowed_actions

        return False