import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senior_buddy_project.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from senior_buddy.models import (
    User, Role, UserRole,
    SeniorProfile, CaregiverProfile, FamilyProfile, VolunteerProfile,
    SeniorCaregiver, SeniorFamily, SeniorVolunteer,
    Doctor, SeniorDoctor,
    Reminder, HealthNote,
    SOSRequest,
    CommunityEvent, EventAttendance,
    ChatMessage, ActivityLog,
)

# =====================================================
# CLEAR EXISTING TEST DATA
# =====================================================
print("Clearing old data...")
ActivityLog.objects.all().delete()
ChatMessage.objects.all().delete()
EventAttendance.objects.all().delete()
CommunityEvent.objects.all().delete()
SOSRequest.objects.all().delete()
HealthNote.objects.all().delete()
Reminder.objects.all().delete()
SeniorDoctor.objects.all().delete()
Doctor.objects.all().delete()
SeniorVolunteer.objects.all().delete()
SeniorFamily.objects.all().delete()
SeniorCaregiver.objects.all().delete()
VolunteerProfile.objects.all().delete()
FamilyProfile.objects.all().delete()
CaregiverProfile.objects.all().delete()
SeniorProfile.objects.all().delete()
UserRole.objects.all().delete()
User.objects.filter(is_superuser=False).delete()
print("Done.")

# =====================================================
# FETCH ROLES
# =====================================================
r_senior    = Role.objects.get(role_name='SENIOR')
r_caregiver = Role.objects.get(role_name='CAREGIVER')
r_family    = Role.objects.get(role_name='FAMILY')
r_volunteer = Role.objects.get(role_name='VOLUNTEER')
r_admin     = Role.objects.get(role_name='ADMIN')

# =====================================================
# CREATE USERS
# =====================================================
def make_user(name, email, phone):
    u = User(full_name=name, email=email, phone=phone, username=email)
    u.set_password('test1234')
    u.save()
    return u

s1 = make_user('Senior 1', 's1@test.com', '1111111111')
s2 = make_user('Senior 2', 's2@test.com', '1111111112')

c1 = make_user('Caregiver 1', 'c1@test.com', '2222222221')
c2 = make_user('Caregiver 2', 'c2@test.com', '2222222222')

f1 = make_user('Family 1', 'f1@test.com', '3333333331')
f2 = make_user('Family 2', 'f2@test.com', '3333333332')

v1 = make_user('Volunteer 1', 'v1@test.com', '4444444441')
v2 = make_user('Volunteer 2', 'v2@test.com', '4444444442')

print("Users created.")

# =====================================================
# ASSIGN ROLES
# =====================================================
UserRole.objects.create(user=s1, role=r_senior)
UserRole.objects.create(user=s2, role=r_senior)
UserRole.objects.create(user=c1, role=r_caregiver)
UserRole.objects.create(user=c2, role=r_caregiver)
UserRole.objects.create(user=f1, role=r_family)
UserRole.objects.create(user=f2, role=r_family)
UserRole.objects.create(user=v1, role=r_volunteer)
UserRole.objects.create(user=v2, role=r_volunteer)

print("Roles assigned.")

# =====================================================
# PROFILES
# =====================================================
SeniorProfile.objects.create(senior=s1, age=65, medical_history='Test history 1', emergency_contact='1000000001')
SeniorProfile.objects.create(senior=s2, age=70, medical_history='Test history 2', emergency_contact='1000000002')

CaregiverProfile.objects.create(caregiver=c1, qualification='Test Qual 1', experience_years=2)
CaregiverProfile.objects.create(caregiver=c2, qualification='Test Qual 2', experience_years=5)

FamilyProfile.objects.create(family=f1, relation='Son')
FamilyProfile.objects.create(family=f2, relation='Daughter')

VolunteerProfile.objects.create(volunteer=v1, skills='Test skill 1', availability='Weekdays', is_verified=True)
VolunteerProfile.objects.create(volunteer=v2, skills='Test skill 2', availability='Weekends', is_verified=False)

print("Profiles created.")

# =====================================================
# RELATIONSHIPS
# =====================================================
SeniorCaregiver.objects.create(senior=s1, caregiver=c1, is_primary=True)
SeniorCaregiver.objects.create(senior=s2, caregiver=c2, is_primary=True)

SeniorFamily.objects.create(senior=s1, family=f1)
SeniorFamily.objects.create(senior=s2, family=f2)

SeniorVolunteer.objects.create(senior=s1, volunteer=v1, assigned_by=f1)
SeniorVolunteer.objects.create(senior=s2, volunteer=v2, assigned_by=f2)

print("Relationships created.")

# =====================================================
# DOCTORS
# =====================================================
d1 = Doctor.objects.create(full_name='Dr Test 1', specialization='General', phone='5555555551', hospital_name='Test Hospital 1', added_by=f1)
d2 = Doctor.objects.create(full_name='Dr Test 2', specialization='Cardiology', phone='5555555552', hospital_name='Test Hospital 2', added_by=f2)

SeniorDoctor.objects.create(senior=s1, doctor=d1, is_primary=True, added_by=f1)
SeniorDoctor.objects.create(senior=s2, doctor=d2, is_primary=True, added_by=f2)

print("Doctors created.")

# =====================================================
# REMINDERS
# =====================================================
Reminder.objects.create(senior=s1, created_by=c1, title='Test Reminder 1', reminder_type='MEDICATION',  reminder_time=timezone.now() + timedelta(hours=2))
Reminder.objects.create(senior=s1, created_by=f1, title='Test Reminder 2', reminder_type='APPOINTMENT', reminder_time=timezone.now() + timedelta(days=1))
Reminder.objects.create(senior=s2, created_by=c2, title='Test Reminder 3', reminder_type='DAILY_TASK',  reminder_time=timezone.now() + timedelta(hours=5), is_completed=True)

print("Reminders created.")

# =====================================================
# HEALTH NOTES
# =====================================================
HealthNote.objects.create(senior=s1, written_by=c1, note_text='Test note 1 for senior 1')
HealthNote.objects.create(senior=s2, written_by=c2, note_text='Test note 1 for senior 2')

print("Health notes created.")

# =====================================================
# SOS REQUESTS
# =====================================================
SOSRequest.objects.create(senior=s1, status='PENDING')
SOSRequest.objects.create(senior=s2, status='IN_PROGRESS', handled_by=c2)
SOSRequest.objects.create(senior=s1, status='RESOLVED',    handled_by=c1, resolved_at=timezone.now())

print("SOS requests created.")

# =====================================================
# COMMUNITY EVENTS
# =====================================================
e1 = CommunityEvent.objects.create(title='Test Event 1', location='Hall A',   event_date=timezone.now() + timedelta(days=3),  created_by=v1)
e2 = CommunityEvent.objects.create(title='Test Event 2', location='Hall B',   event_date=timezone.now() + timedelta(days=7),  created_by=v2)
e3 = CommunityEvent.objects.create(title='Test Event 3', location='Online',   event_date=timezone.now() + timedelta(days=14), created_by=f1)

EventAttendance.objects.create(event=e1, user=s1, status='REGISTERED')
EventAttendance.objects.create(event=e1, user=s2, status='ATTENDED')
EventAttendance.objects.create(event=e2, user=v1, status='REGISTERED')
EventAttendance.objects.create(event=e3, user=s1, status='CANCELLED')

print("Events created.")

# =====================================================
# CHAT MESSAGES
# =====================================================
ChatMessage.objects.create(sender=s1, receiver=c1, message='Test message 1', is_read=True)
ChatMessage.objects.create(sender=c1, receiver=s1, message='Test reply 1',   is_read=False)
ChatMessage.objects.create(sender=f1, receiver=c1, message='Test message 2', is_read=True)
ChatMessage.objects.create(sender=s2, receiver=f2, message='Test message 3', is_read=False)

print("Chat messages created.")

# =====================================================
# ACTIVITY LOGS
# =====================================================
ActivityLog.objects.create(senior=s1, performed_by=c1, log_type='CAREGIVER_ACTION', action='MEDICATION_GIVEN',  notes='Test note')
ActivityLog.objects.create(senior=s1, performed_by=c1, log_type='CAREGIVER_ACTION', action='VITALS_CHECKED',   notes='Test note')
ActivityLog.objects.create(senior=s2, performed_by=v1, log_type='VOLUNTEER_VISIT',  action='VISIT_COMPLETED',  notes='Test note')
ActivityLog.objects.create(senior=s2, performed_by=v2, log_type='VOLUNTEER_VISIT',  action='VISIT_COMPLETED',  notes='Test note')

print("Activity logs created.")

print("")
print("All dummy data created successfully.")
print("Login with any test user:")
print("  Email:    s1@test.com  (Senior)")
print("  Email:    c1@test.com  (Caregiver)")
print("  Email:    f1@test.com  (Family)")
print("  Email:    v1@test.com  (Volunteer)")
print("  Password: test1234")
