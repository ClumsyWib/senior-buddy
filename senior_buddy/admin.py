from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone

from .models import (
    User, Role, UserRole,
    SeniorProfile, CaregiverProfile, FamilyProfile, VolunteerProfile,
    SeniorCaregiver, SeniorFamily, SeniorVolunteer,
    Doctor, SeniorDoctor,
    Reminder, HealthNote,
    SOSRequest,
    CommunityEvent, EventAttendance,
    ChatMessage,
    ActivityLog,
)


# =====================================================
# SENIOR BUDDY — admin.py
# =====================================================


# =====================================================
# USER & ROLE
# =====================================================

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display  = ('role_id', 'role_name')
    search_fields = ('role_name',)


class UserRoleInline(admin.TabularInline):
    """Show assigned roles inside the User edit page."""
    model   = UserRole
    extra   = 1
    fields  = ('role',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines     = [UserRoleInline]
    list_display  = ('id', 'full_name', 'email', 'phone', 'role_badges', 'is_active', 'created_at')
    list_filter   = ('is_active', 'is_staff')
    search_fields = ('full_name', 'email', 'phone')
    ordering      = ('-created_at',)
    readonly_fields = ('created_at', 'last_login', 'date_joined')

    # Add our fields to the default Django fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Senior Buddy', {
            'fields': ('full_name', 'phone', 'created_at')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Senior Buddy', {
            'fields': ('full_name', 'email', 'phone')
        }),
    )

    @admin.display(description='Roles')
    def role_badges(self, obj):
        colours = {
            'ADMIN':     '#e74c3c',
            'SENIOR':    '#3498db',
            'CAREGIVER': '#2ecc71',
            'FAMILY':    '#f39c12',
            'VOLUNTEER': '#9b59b6',
        }
        roles = UserRole.objects.filter(user=obj).select_related('role')
        badges = []
        for ur in roles:
            colour = colours.get(ur.role.role_name, '#95a5a6')
            badges.append(
                f'<span style="background:{colour};color:#fff;padding:2px 8px;'
                f'border-radius:4px;font-size:11px;margin-right:3px;">'
                f'{ur.role.role_name}</span>'
            )
        return format_html(''.join(badges)) if badges else '—'


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'role')
    list_filter   = ('role',)
    search_fields = ('user__full_name', 'user__email')


# =====================================================
# PROFILE TABLES
# =====================================================

@admin.register(SeniorProfile)
class SeniorProfileAdmin(admin.ModelAdmin):
    list_display  = ('senior', 'age', 'emergency_contact', 'has_medical_history')
    search_fields = ('senior__full_name', 'emergency_contact')
    readonly_fields = ('senior',)

    @admin.display(description='Medical History?', boolean=True)
    def has_medical_history(self, obj):
        return bool(obj.medical_history)


@admin.register(CaregiverProfile)
class CaregiverProfileAdmin(admin.ModelAdmin):
    list_display  = ('caregiver', 'qualification', 'experience_years')
    search_fields = ('caregiver__full_name', 'qualification')
    readonly_fields = ('caregiver',)


@admin.register(FamilyProfile)
class FamilyProfileAdmin(admin.ModelAdmin):
    list_display  = ('family', 'relation')
    search_fields = ('family__full_name', 'relation')
    list_filter   = ('relation',)
    readonly_fields = ('family',)


@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display  = ('volunteer', 'availability', 'is_verified')
    search_fields = ('volunteer__full_name', 'skills')
    list_filter   = ('is_verified',)
    readonly_fields = ('volunteer',)
    actions = ['mark_verified', 'mark_unverified']

    @admin.action(description='Mark selected as Verified')
    def mark_verified(self, request, queryset):
        count = queryset.update(is_verified=True)
        self.message_user(request, f'{count} volunteer(s) marked as verified.')

    @admin.action(description='Mark selected as Unverified')
    def mark_unverified(self, request, queryset):
        count = queryset.update(is_verified=False)
        self.message_user(request, f'{count} volunteer(s) marked as unverified.')


# =====================================================
# RELATIONSHIP TABLES
# =====================================================

@admin.register(SeniorCaregiver)
class SeniorCaregiverAdmin(admin.ModelAdmin):
    list_display  = ('id', 'senior', 'caregiver', 'is_primary', 'assigned_by', 'assigned_at')
    list_filter   = ('is_primary',)
    search_fields = ('senior__full_name', 'caregiver__full_name')
    readonly_fields = ('assigned_at',)


@admin.register(SeniorFamily)
class SeniorFamilyAdmin(admin.ModelAdmin):
    list_display  = ('id', 'senior', 'family', 'added_at')
    search_fields = ('senior__full_name', 'family__full_name')
    readonly_fields = ('added_at',)


@admin.register(SeniorVolunteer)
class SeniorVolunteerAdmin(admin.ModelAdmin):
    list_display  = ('id', 'senior', 'volunteer', 'assigned_by', 'assigned_at')
    search_fields = ('senior__full_name', 'volunteer__full_name')
    readonly_fields = ('assigned_at',)


# =====================================================
# DOCTOR MODULE
# =====================================================

class SeniorDoctorInline(admin.TabularInline):
    """Show linked seniors inside Doctor edit page."""
    model   = SeniorDoctor
    extra   = 0
    fields  = ('senior', 'is_primary', 'added_at')
    readonly_fields = ('added_at',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display  = ('doctor_id', 'full_name', 'specialization', 'phone', 'hospital_name', 'added_by')
    search_fields = ('full_name', 'specialization', 'hospital_name')
    list_filter   = ('specialization',)
    inlines       = [SeniorDoctorInline]


@admin.register(SeniorDoctor)
class SeniorDoctorAdmin(admin.ModelAdmin):
    list_display  = ('id', 'senior', 'doctor', 'is_primary', 'added_by', 'added_at')
    list_filter   = ('is_primary',)
    search_fields = ('senior__full_name', 'doctor__full_name')
    readonly_fields = ('added_at',)


# =====================================================
# REMINDER SYSTEM
# =====================================================

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display  = ('reminder_id', 'title', 'senior', 'created_by', 'reminder_type', 'reminder_time', 'is_completed')
    list_filter   = ('reminder_type', 'is_completed')
    search_fields = ('title', 'senior__full_name', 'created_by__full_name')
    readonly_fields = ('created_at',)
    date_hierarchy  = 'reminder_time'
    actions = ['mark_completed', 'mark_pending']

    @admin.action(description='Mark selected as Completed')
    def mark_completed(self, request, queryset):
        count = queryset.update(is_completed=True)
        self.message_user(request, f'{count} reminder(s) marked as completed.')

    @admin.action(description='Mark selected as Pending')
    def mark_pending(self, request, queryset):
        count = queryset.update(is_completed=False)
        self.message_user(request, f'{count} reminder(s) marked as pending.')


# =====================================================
# HEALTH NOTES
# =====================================================

@admin.register(HealthNote)
class HealthNoteAdmin(admin.ModelAdmin):
    list_display  = ('note_id', 'senior', 'written_by', 'note_preview', 'created_at')
    search_fields = ('senior__full_name', 'written_by__full_name', 'note_text')
    readonly_fields = ('created_at',)
    date_hierarchy  = 'created_at'

    @admin.display(description='Note Preview')
    def note_preview(self, obj):
        return obj.note_text[:60] + '...' if len(obj.note_text) > 60 else obj.note_text


# =====================================================
# SOS SYSTEM
# =====================================================

@admin.register(SOSRequest)
class SOSRequestAdmin(admin.ModelAdmin):
    list_display  = ('sos_id', 'senior', 'status_badge', 'triggered_at', 'handled_by', 'escalated_by', 'resolved_at')
    list_filter   = ('status',)
    search_fields = ('senior__full_name', 'handled_by__full_name')
    readonly_fields = ('triggered_at',)
    date_hierarchy  = 'triggered_at'
    actions = ['mark_in_progress', 'mark_resolved']

    @admin.display(description='Status')
    def status_badge(self, obj):
        colours = {
            'PENDING':     '#e74c3c',
            'IN_PROGRESS': '#f39c12',
            'RESOLVED':    '#2ecc71',
        }
        colour = colours.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;'
            'border-radius:4px;font-size:11px;">{}</span>',
            colour, obj.status
        )

    @admin.action(description='Mark selected as In Progress')
    def mark_in_progress(self, request, queryset):
        count = queryset.update(status='IN_PROGRESS')
        self.message_user(request, f'{count} SOS request(s) marked as in progress.')

    @admin.action(description='Mark selected as Resolved')
    def mark_resolved(self, request, queryset):
        count = queryset.update(status='RESOLVED', resolved_at=timezone.now())
        self.message_user(request, f'{count} SOS request(s) marked as resolved.')


# =====================================================
# COMMUNITY EVENTS
# =====================================================

class EventAttendanceInline(admin.TabularInline):
    """Show attendance list inside Event edit page."""
    model   = EventAttendance
    extra   = 0
    fields  = ('user', 'status', 'joined_at')
    readonly_fields = ('joined_at',)


@admin.register(CommunityEvent)
class CommunityEventAdmin(admin.ModelAdmin):
    list_display  = ('event_id', 'title', 'location', 'event_date', 'created_by', 'attendee_count')
    search_fields = ('title', 'location', 'created_by__full_name')
    readonly_fields = ('created_at',)
    date_hierarchy  = 'event_date'
    inlines         = [EventAttendanceInline]

    @admin.display(description='Attendees')
    def attendee_count(self, obj):
        return obj.attendances.exclude(status='CANCELLED').count()


@admin.register(EventAttendance)
class EventAttendanceAdmin(admin.ModelAdmin):
    list_display  = ('id', 'event', 'user', 'status', 'joined_at')
    list_filter   = ('status',)
    search_fields = ('event__title', 'user__full_name')
    readonly_fields = ('joined_at',)


# =====================================================
# CHAT SYSTEM
# =====================================================

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display  = ('message_id', 'sender', 'receiver', 'message_preview', 'is_read', 'sent_at')
    list_filter   = ('is_read',)
    search_fields = ('sender__full_name', 'receiver__full_name')
    readonly_fields = ('sent_at',)
    date_hierarchy  = 'sent_at'

    @admin.display(description='Message Preview')
    def message_preview(self, obj):
        return obj.message[:60] + '...' if len(obj.message) > 60 else obj.message


# =====================================================
# ACTIVITY LOG
# =====================================================

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display  = ('log_id', 'performed_by', 'senior', 'log_type', 'action', 'created_at')
    list_filter   = ('log_type',)
    search_fields = ('performed_by__full_name', 'senior__full_name', 'action')
    readonly_fields = ('created_at',)
    date_hierarchy  = 'created_at'

    # Logs should never be edited
    def has_change_permission(self, request, obj=None):
        return False

    # Only superuser can delete logs
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
