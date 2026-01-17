from django.contrib import admin
from events.models import Event, Venue, Favorite
from django.contrib.auth.models import User

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at', ]
    search_fields = ['name']
    readonly_fields = ['created_at']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','start_date', 'end_date', 'is_completed', 'venue', 'manager', 'display_attendees')
    autocomplete_fields = ('manager','attendees')
    list_filter = ('is_completed', 'venue')
    ordering = ('-start_date',)
    list_select_related = ('venue','manager')
    search_fields = ('manager','title',)

    def display_attendees(self, obj):
        return ", ".join([str(attendee) for attendee in obj.attendees.all()])
    display_attendees.short_description = 'Attendees'

class EventInline(admin.StackedInline):
    model = Event
    extra = 0
    autocomplete_fields = ['manager']

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'web', 'owner')
    list_filter = ('owner',)
    ordering = ('name',)
    search_fields = ('name', )
    inlines = [EventInline]
