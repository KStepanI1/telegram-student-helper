from django.contrib import admin

from .models import User, Subjects, ZoomLinks, Teachers, Timetable


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "name", "username", "created_at")


@admin.register(Subjects)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(ZoomLinks)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "type")


@admin.register(Teachers)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "middle_name", "subject", "type")


@admin.register(Timetable)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "weekday")
