from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extended user profile with weather preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='weather_profile')
    default_city = models.CharField(max_length=100, blank=True, null=True, help_text="User's default city for weather")
    email_verified = models.BooleanField(default=False)
    preferences = models.JSONField(default=dict, blank=True, help_text="User weather preferences (units, etc)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class SavedCity(models.Model):
    """User's saved cities for quick weather lookups"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_cities')
    city_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    is_default = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Saved City"
        verbose_name_plural = "Saved Cities"
        unique_together = ('user', 'city_name')
    
    def __str__(self):
        return f"{self.city_name} ({self.user.username})"
