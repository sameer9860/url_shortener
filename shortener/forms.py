from django import forms
from .models import ShortURL

# Create URL Form
class CreateURLForm(forms.ModelForm):
    custom_key = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' my-brand ',
            'maxlength': '10'
        }),
        help_text='Max 10 characters. Leave blank to auto-generate. Only letters, numbers, and hyphens.'
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
        import re
        key = self.cleaned_data.get('custom_key', '').strip()
        if not key:
            return key
        # Max 10 characters (matches short_key DB column limit)
        if len(key) > 10:
            raise forms.ValidationError('Custom key cannot exceed 10 characters.')
        # Only allow letters, numbers, hyphens
        if not re.match(r'^[a-zA-Z0-9\-]+$', key):
            raise forms.ValidationError('Only letters, numbers, and hyphens are allowed.')
        # Check if already taken
        if ShortURL.objects.filter(short_key=key).exists() or ShortURL.objects.filter(custom_key=key).exists():
            raise forms.ValidationError(f'"{key}" is already taken. Please choose a different key.')
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