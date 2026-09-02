from django.contrib import admin
from django.utils.html import format_html
from .models import CurrentWeather, WeatherHistory, WeatherAlert, Notification


@admin.register(CurrentWeather)
class CurrentWeatherAdmin(admin.ModelAdmin):
    list_display = ('city', 'country', 'temperature_display', 'condition', 'humidity_percent', 'created_at')
    list_filter = ('country', 'condition', 'created_at')
    search_fields = ('city', 'country')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    def temperature_display(self, obj):
        return f"{obj.temperature}°C"
    temperature_display.short_description = "Temperature"
    
    def humidity_percent(self, obj):
        return f"{obj.humidity}%"
    humidity_percent.short_description = "Humidity"


@admin.register(WeatherHistory)
class WeatherHistoryAdmin(admin.ModelAdmin):
    list_display = ('city', 'user', 'temperature', 'condition', 'date')
    list_filter = ('city', 'date', 'condition')
    search_fields = ('city', 'user__username')
    date_hierarchy = 'date'
    readonly_fields = ('recorded_at', 'date')
    
    fieldsets = (
        ('User & Location', {
            'fields': ('user', 'city')
        }),
        ('Weather Data', {
            'fields': ('temperature', 'feels_like', 'humidity', 'condition', 'wind_speed')
        }),
        ('Timestamps', {
            'fields': ('recorded_at', 'date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WeatherAlert)
class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'alert_type_badge', 'condition', 'is_active', 'created_at')
    list_filter = ('alert_type', 'is_active', 'created_at')
    search_fields = ('user__username', 'city')
    readonly_fields = ('created_at',)
    
    def alert_type_badge(self, obj):
        colors = {
            'heat': '#ff6b6b',
            'cold': '#0099ff',
            'rain': '#00d4ff',
            'wind': '#ffa500',
            'storm': '#ff0000',
        }
        color = colors.get(obj.alert_type, '#666')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_alert_type_display()
        )
    alert_type_badge.short_description = "Alert Type"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'read_status', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    readonly_fields = ('created_at',)
    
    def read_status(self, obj):
        status = "✓ Read" if obj.is_read else "Unread"
        color = '#28a745' if obj.is_read else '#dc3545'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status
        )
    read_status.short_description = "Status"
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notification(s) marked as read.")
    mark_as_read.short_description = "Mark selected as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} notification(s) marked as unread.")
    mark_as_unread.short_description = "Mark selected as unread"
