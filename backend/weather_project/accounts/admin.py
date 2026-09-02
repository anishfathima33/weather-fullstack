from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, SavedCity


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'default_city', 'email_verified_badge', 'created_at')
    list_filter = ('email_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'default_city')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Preferences', {
            'fields': ('default_city', 'preferences')
        }),
        ('Verification', {
            'fields': ('email_verified',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def username(self, obj):
        return obj.user.username
    username.short_description = "Username"
    
    def email(self, obj):
        return obj.user.email
    email.short_description = "Email"
    
    def email_verified_badge(self, obj):
        if obj.email_verified:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">✓ Verified</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">Not Verified</span>'
        )
    email_verified_badge.short_description = "Email Status"


@admin.register(SavedCity)
class SavedCityAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'country', 'user', 'is_default', 'added_at')
    list_filter = ('is_default', 'added_at')
    search_fields = ('city_name', 'country', 'user__username')
    date_hierarchy = 'added_at'
    readonly_fields = ('added_at',)
    
    actions = ['set_as_default', 'unset_as_default']
    
    def set_as_default(self, request, queryset):
        for saved_city in queryset:
            SavedCity.objects.filter(user=saved_city.user).update(is_default=False)
            saved_city.is_default = True
            saved_city.save()
        self.message_user(request, "Selected cities set as default.")
    set_as_default.short_description = "Set as default city"
    
    def unset_as_default(self, request, queryset):
        queryset.update(is_default=False)
        self.message_user(request, "Selected cities unset as default.")
    unset_as_default.short_description = "Unset as default city"
