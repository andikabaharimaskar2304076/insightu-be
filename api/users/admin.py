from django.contrib import admin
from .models import PsychologistProfile, PsychologistAvailability

@admin.register(PsychologistProfile)
class PsychologistProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')  # Show UUID

@admin.register(PsychologistAvailability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'psychologist', 'day_of_week', 'start_time', 'end_time')
    readonly_fields = ('id',)  # Make UUID visible in form view
