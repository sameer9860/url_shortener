from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import ShortURL, Click
from .forms import CreateURLForm, EditURLForm
from .utils import unique_short_key, generate_qr_code, is_expired


# Dashboard
@login_required
def dashboard(request):
    urls = ShortURL.objects.filter(user=request.user)
    return render(request, 'shortener/dashboard.html', {'urls': urls})


# Create URL
@login_required
def create_url(request):
    if request.method == 'POST':
        form = CreateURLForm(request.POST)
        if form.is_valid():
            short_url = form.save(commit=False)
            short_url.user = request.user

            # Use custom key if provided, otherwise auto-generate
            custom_key = form.cleaned_data.get('custom_key', '').strip()
            if custom_key:
                short_url.short_key = custom_key
                short_url.custom_key = custom_key
            else:
                short_url.short_key = unique_short_key()

            short_url.save()

            # Generate QR code if requested
            if form.cleaned_data.get('generate_qr'):
                generate_qr_code(short_url, request)

            messages.success(request, f'Short URL created successfully!')
            return redirect('shortener:dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CreateURLForm()

    return render(request, 'shortener/create_url.html', {'form': form})


# Edit URL
@login_required
def edit_url(request, pk):
    short_url = get_object_or_404(ShortURL, pk=pk, user=request.user)

    if request.method == 'POST':
        form = EditURLForm(request.POST, instance=short_url)
        if form.is_valid():
            form.save()
            messages.success(request, 'URL updated successfully!')
            return redirect('shortener:dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = EditURLForm(instance=short_url)

    return render(request, 'shortener/edit_url.html', {
        'form': form,
        'short_url': short_url
    })


# Delete URL
@login_required
def delete_url(request, pk):
    short_url = get_object_or_404(ShortURL, pk=pk, user=request.user)

    if request.method == 'POST':
        short_url.delete()
        messages.success(request, 'Short URL deleted successfully!')
        return redirect('shortener:dashboard')

    return render(request, 'shortener/delete_confirm.html', {'short_url': short_url})


# Detail / Analytics
@login_required
def url_detail(request, pk):
    short_url = get_object_or_404(ShortURL, pk=pk, user=request.user)

    clicks_last_7_days = short_url.clicks.filter(
        clicked_at__gte=timezone.now() - timedelta(days=7)
    ).count()

    clicks_last_30_days = short_url.clicks.filter(
        clicked_at__gte=timezone.now() - timedelta(days=30)
    ).count()

    recent_clicks = short_url.clicks.all()[:10]

    return render(request, 'shortener/url_detail.html', {
        'short_url': short_url,
        'clicks_last_7_days': clicks_last_7_days,
        'clicks_last_30_days': clicks_last_30_days,
        'recent_clicks': recent_clicks,
    })


# Redirect (public)
def redirect_url(request, short_key):
    short_url = get_object_or_404(ShortURL, short_key=short_key, is_active=True)

    if is_expired(short_url):
        return render(request, 'shortener/expired.html', {'short_url': short_url})

    # Log the click
    Click.objects.create(
        short_url=short_url,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    short_url.click_count += 1
    short_url.save(update_fields=['click_count'])

    return redirect(short_url.original_url)