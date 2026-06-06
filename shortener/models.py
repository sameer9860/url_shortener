from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.conf import settings

# Short URL Model
class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='short_urls')
    original_url = models.URLField(max_length=2000)
    short_key = models.CharField(max_length=10,unique=True,db_index=True)
    custom_key  = models.CharField(max_length=20,null=True,blank=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True,blank=True)
    is_active  = models.BooleanField(default=True)
    click_count = models.PositiveIntegerField(default=0)
    qr_code = models.ImageField(upload_to='qr_codes/',null=True,blank=True)

    class Meta :
        ordering = ['-created_at']

    def __str__(self):
        return self.short_key
        
# Click Model
class Click(models.Model):
    short_url = models.ForeignKey(ShortURL,on_delete=models.CASCADE,related_name="clicks")
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True,blank=True)
    user_agent = models.TextField(null=True,blank=True)

    class Meta :
        ordering = ['-clicked_at']

    def __str__(self):
        return f"{self.short_url.short_key} - {self.clicked_at}"