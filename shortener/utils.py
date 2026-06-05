import random,string
import qrcode,os
from django.conf import settings
from django.utils import timezone


BASE62 = string.ascii_letters + string.digits   

def generate_short_key(length=6):
    return ''.join(random.choices(BASE62, k=length))

def unique_short_key():
    from .models import ShortURL
    while True:
        key = generate_short_key()
        if not ShortURL.objects.filter(short_key=key).exists():
            return key

def generate_qr_code(short_url_obj,request):
    full_url = request.build_absolute_uri(f'/{short_url_obj.short_key}/')
    img = qrcode.make(full_url)
    path = f'qrcodes/{short_url_obj.short_key}.png'
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    img.save(full_path)
    short_url_obj.qr_code = path
    short_url_obj.save()
    

def is_expired(short_url_obj):
    if short_url_obj.expires_at:
        return timezone.now() > short_url_obj.expires_at
    return False           