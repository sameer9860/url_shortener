from django.contrib import admin
from .models import ShortURL,Click

# Register your models here.
@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ['short_key', 'original_url', 'created_at', 'click_count']
    list_filter = ['created_at', 'is_active']
    search_fields = ['short_key', 'original_url']


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ['short_url', 'clicked_at', 'ip_address']
    list_filter = ['clicked_at', 'ip_address']
    search_fields = ['short_url__short_key', 'ip_address']
