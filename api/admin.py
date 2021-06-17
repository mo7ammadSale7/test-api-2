from django.contrib import admin

from .models import Meal, Rating


class MealAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    list_filter = ['title']
    search_fields = ['title', 'description']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'meal', 'user', 'stars']
    list_filter = ['meal', 'user']


admin.site.register(Meal, MealAdmin)
admin.site.register(Rating, RatingAdmin)
