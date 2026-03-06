from rest_framework.permissions import BasePermission
from .models import UserRole


# =====================================================
# SENIOR BUDDY — permissions.py
# Role-based access control for API endpoints
# =====================================================

def get_user_roles(user):
    """Return a list of role names for a given user."""
    return list(
        UserRole.objects.filter(user=user)
        .values_list('role__role_name', flat=True)
    )


class IsAdmin(BasePermission):
    """Only Admin users can access this endpoint."""
    def has_permission(self, request, view):
        return 'ADMIN' in get_user_roles(request.user)


class IsSenior(BasePermission):
    """Only Senior users can access this endpoint."""
    def has_permission(self, request, view):
        return 'SENIOR' in get_user_roles(request.user)


class IsCaregiver(BasePermission):
    """Only Caregiver users can access this endpoint."""
    def has_permission(self, request, view):
        return 'CAREGIVER' in get_user_roles(request.user)


class IsFamily(BasePermission):
    """Only Family users can access this endpoint."""
    def has_permission(self, request, view):
        return 'FAMILY' in get_user_roles(request.user)


class IsVolunteer(BasePermission):
    """Only Volunteer users can access this endpoint."""
    def has_permission(self, request, view):
        return 'VOLUNTEER' in get_user_roles(request.user)


class IsAdminOrFamily(BasePermission):
    """Admin or Family members can access this endpoint."""
    def has_permission(self, request, view):
        roles = get_user_roles(request.user)
        return 'ADMIN' in roles or 'FAMILY' in roles


class IsAdminOrCaregiver(BasePermission):
    """Admin or Caregiver can access this endpoint."""
    def has_permission(self, request, view):
        roles = get_user_roles(request.user)
        return 'ADMIN' in roles or 'CAREGIVER' in roles


class IsCaregiverOrFamily(BasePermission):
    """Caregiver or Family can access this endpoint."""
    def has_permission(self, request, view):
        roles = get_user_roles(request.user)
        return 'CAREGIVER' in roles or 'FAMILY' in roles


class IsNotVolunteer(BasePermission):
    """
    Anyone EXCEPT Volunteers.
    Used to block volunteers from seeing medical data.
    """
    def has_permission(self, request, view):
        return 'VOLUNTEER' not in get_user_roles(request.user)


class IsSeniorOrCaregiverOrFamily(BasePermission):
    """Senior, Caregiver, or Family — for reminder creation."""
    def has_permission(self, request, view):
        roles = get_user_roles(request.user)
        return bool({'SENIOR', 'CAREGIVER', 'FAMILY'} & set(roles))
