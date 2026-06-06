from django import forms
from .models import ShortURL

# Create URL Form
class CreateURLForm(forms.ModelForm):
    custom_key = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. my-brand (optional)'
        }),
        help_text='Leave blank to auto-generate. Only letters, numbers, and hyphens.'
    )
    expires_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        help_text='Leave blank for no expiration.',
        input_formats=['%Y-%m-%dT%H:%M']
    )
    generate_qr = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Generate a QR code for this URL.'
    )

    class Meta:
        model = ShortURL
        fields = ['original_url', 'custom_key', 'expires_at', 'generate_qr']
        widgets = {
            'original_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/very/long/url'
            })
        }

    def clean_custom_key(self):
        key = self.cleaned_data.get('custom_key', '').strip()
        if not key:
            return key
        # Only allow letters, numbers, hyphens
        import re
        if not re.match(r'^[a-zA-Z0-9\-]+$', key):
            raise forms.ValidationError('Only letters, numbers, and hyphens are allowed.')
        # Check uniqueness against both short_key and custom_key columns
        if ShortURL.objects.filter(short_key=key).exists():
            raise forms.ValidationError('This key is already taken. Please choose another.')
        if ShortURL.objects.filter(custom_key=key).exists():
            raise forms.ValidationError('This custom key is already taken. Please choose another.')
        return key


# Edit URL Form
class EditURLForm(forms.ModelForm):
    expires_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        help_text='Leave blank for no expiration.',
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = ShortURL
        fields = ['original_url', 'expires_at', 'is_active']
        widgets = {
            'original_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/very/long/url'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }