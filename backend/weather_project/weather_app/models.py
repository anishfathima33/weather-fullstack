from django.db import models
from django.contrib.auth.models import User

class CurrentWeather(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    min_temp = models.FloatField()
    max_temp = models.FloatField()
    condition = models.CharField(max_length=50)
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    advice = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city


class WeatherHistory(models.Model):
    """Historical weather data for trends and analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weather_history')
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    humidity = models.IntegerField()
    condition = models.CharField(max_length=50)
    wind_speed = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Weather History"
        verbose_name_plural = "Weather Histories"
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['city', 'date']),
        ]
    
    def __str__(self):
        return f"{self.city} - {self.date}"


class WeatherAlert(models.Model):
    """Alerts for extreme weather conditions"""
    ALERT_TYPES = (
        ('heat', 'Extreme Heat'),
        ('cold', 'Extreme Cold'),
        ('rain', 'Heavy Rain'),
        ('wind', 'Strong Wind'),
        ('storm', 'Storm Warning'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weather_alerts')
    city = models.CharField(max_length=100)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    temperature = models.FloatField(blank=True, null=True)
    condition = models.CharField(max_length=50)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Weather Alert"
        verbose_name_plural = "Weather Alerts"
    
    def __str__(self):
        return f"Alert: {self.alert_type} in {self.city}"


class Notification(models.Model):
    """In-app notifications for users"""
    NOTIFICATION_TYPES = (
        ('weather_alert', 'Weather Alert'),
        ('weather_update', 'Weather Update'),
        ('system', 'System Notification'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True, help_text="Additional notification data")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Forecast(models.Model):
    weather = models.ForeignKey(CurrentWeather, on_delete=models.CASCADE, related_name="forecast")
    date = models.DateField()
    min_temp = models.FloatField()
    max_temp = models.FloatField()
    condition = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.weather.city} - {self.date}"