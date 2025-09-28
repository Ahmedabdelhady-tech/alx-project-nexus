from django.contrib import admin
from .models import Category, Job, Application


class ApplicationInline(admin.TabularInline):

    model = Application
    extra = 0
    readonly_fields = ("candidate", "applied_at", "status")
    can_delete = False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")
    inlines = [ApplicationInline]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "candidate", "job", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("candidate__username", "job__title")
    readonly_fields = ("applied_at",)
