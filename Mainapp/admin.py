from django.contrib import admin
from django.contrib import admin
from .models import Business, NeighbourHood, Profile, Updates



admin.site.register(Profile)
admin.site.register(NeighbourHood)
admin.site.register(Updates)
admin.site.register(Business)

