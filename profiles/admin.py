from django.contrib import admin

from .models import Profile, Film, DiaryEntry


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "display_name", "last_fetched"]
    search_fields = ["username"]


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ["title", "year", "director"]
    search_fields = ["title"]


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ["profile", "film", "rating", "watched_date"]
    list_filter = ["rating"]
