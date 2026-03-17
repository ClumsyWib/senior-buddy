from rest_framework.permissions import BasePermission
from .models import UserRole


# =====================================================
# SENIOR BUDDY — permissions.py
# Role-based access control for API endpoints
# =====================================================

def get_user_roles(request):
    """
    Return a list of role names for the current user.
    Caches the result on the request object so multiple
    permission classes on the same view only hit the DB once.
    """
    if not hasattr(request, '_cached_roles'):
        request._cached_roles = list(
            UserRole.objects.filter(user=request.user)
            .values_list('role__role_name', flat=True)
        )
    return request._cached_roles


class IsAdmin(BasePermission):
    """Only Admin users can access this endpoint."""
    def has_permission(self, request, view):
        return 'ADMIN' in get_user_roles(request)


class IsSenior(BasePermission):
    """Only Senior users can access this endpoint."""
    def has_permission(self, request, view):
        return 'SENIOR' in get_user_roles(request)


class IsCaregiver(BasePermission):
    """Only Caregiver users can access this endpoint."""
    def has_permission(self, request, view):
        return 'CAREGIVER' in get_user_roles(request)


class IsFamily(BasePermission):
    """Only Family users can access this endpoint."""
    def has_permission(self, request, view):
        return 'FAMILY' in get_user_roles(request)


class IsVolunteer(BasePermission):
    """Only Volunteer users can access this endpoint."""
    def has_permission(self, request, view):
        return 'VOLUNTEER' in get_user_roles(request)


class IsAdminOrFamily(BasePermission):
    """Admin or Family members can access this endpoint."""
    def has_permission(self, request, view):
        roles = get_user_roles(request)
        return 'ADMIN' in roles or 'FAMILY' in roles


class IsAdminOrCaregiver(BasePermission):
    """Admin or Caregiver can access this endpoint."""
    def has_permission(self, request, view):
        roles = get_user_roles(request)
        return 'ADMIN' in roles or 'CAREGIVER' in roles


class IsCaregiverOrFamily(BasePermission):
    """Caregiver or Family can access this endpoint."""
    def has_permission(self, request, view):
        roles = get_user_roles(request)
        return 'CAREGIVER' in roles or 'FAMILY' in roles


class IsNotVolunteer(BasePermission):
    """
    Anyone EXCEPT Volunteers.
    Used to block volunteers from seeing medical data.
    """
    def has_permission(self, request, view):
        return 'VOLUNTEER' not in get_user_roles(request)


class IsSeniorOrCaregiverOrFamily(BasePermission):
    """Senior, Caregiver, or Family — for reminder creation."""
    def has_permission(self, request, view):
        roles = get_user_roles(request)
        return bool({'SENIOR', 'CAREGIVER', 'FAMILY'} & set(roles))