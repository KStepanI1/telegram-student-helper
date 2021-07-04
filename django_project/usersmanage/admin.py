from django.contrib import admin

from .models import User, Subject, ZoomLink, Teacher, Timetable, Weekday


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "name", "username", "created_at")


@admin.register(Subject)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(ZoomLink)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "type")


@admin.register(Teacher)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "middle_name", "subject", "type")


@admin.register(Timetable)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "weekday", "subject", "lesson_number", "week_parity")


@admin.register(Weekday)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")
