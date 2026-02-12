from rest_framework.permissions import BasePermission


class IsStaffUser(BasePermission):
    """Allow access only to staff or admin users."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.roles.filter(
            role__in=['admin', 'staff']
        ).exists()


class IsAdminUser(BasePermission):
    """Allow access only to admin users."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.roles.filter(role='admin').exists()


class IsStoreStaff(BasePermission):
    """Allow access only to staff assigned to the specific store."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        store_id = view.kwargs.get('store_id')
        if not store_id:
            return False
        return request.user.roles.filter(
            role__in=['admin', 'staff'],
            store_id=store_id
        ).exists() or request.user.roles.filter(role='admin', store__isnull=True).exists()