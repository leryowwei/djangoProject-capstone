import trip.models
from django.contrib import admin

admin.site.register(trip.models.User)
admin.site.register(trip.models.Country)
admin.site.register(trip.models.Budget)
admin.site.register(trip.models.Period)
admin.site.register(trip.models.Category)
admin.site.register(trip.models.Planner)
admin.site.register(trip.models.Attraction)
admin.site.register(trip.models.Itinerary)
