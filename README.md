# Shortly — URL Shortener

A full-featured URL shortener built with Django. Authenticated users can shorten
URLs, track clicks, set expiration dates, customize short keys, and generate QR codes.

---

## Tech Stack

- Python 3.10+
- Django 4.2+
- qrcode + Pillow (QR code generation)

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/sameer9860/url_shortener.git
cd url_shortener  or go to the directory where you have cloned the repository
```

### 2. Create and activate a virtual environment
```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Create a superuser (optional, for admin panel)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser.

---

## Project Structure
shortly/
├── urlshortener/          # Django project config (settings, root urls)
├── accounts/              # User authentication app
│   ├── forms.py           # RegisterForm, LoginForm
│   ├── views.py           # register, login, logout views
│   └── urls.py
├── shortener/             # Core URL shortening app
│   ├── models.py          # ShortURL, Click models
│   ├── forms.py           # CreateURLForm, EditURLForm
│   ├── views.py           # dashboard, create, edit, delete, detail, redirect
│   ├── utils.py           # key generator, QR code, expiry checker
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── accounts/          # login.html, register.html
│   └── shortener/         # dashboard, create, edit, delete, detail, expired
├── media/                 # QR code images (auto-created)
├── requirements.txt
└── README.md

---

## Features

### Core
- User registration, login, and logout
- Shorten any long URL to a base62 short key (e.g. `/aB3kRz`)
- Short URLs redirect instantly to the original URL
- Dashboard listing all your short URLs

### URL Management
- Edit the destination URL or expiration date
- Toggle a URL active/inactive without deleting it
- Delete URLs with a confirmation step

### Analytics
- Click counter on every URL (incremented on each redirect)
- Per-URL detail page showing:
  - Total clicks
  - Clicks in the last 7 days
  - Clicks in the last 30 days
  - Last 10 clicks with timestamp, IP address, and user agent

### Bonus Features
- **Custom short keys** — choose your own key (e.g. `/my-brand`) instead of auto-generated
- **Expiration dates** — set a datetime after which the link shows an expired page
- **QR code generation** — optionally generate a QR code at creation time, downloadable from the detail page

---

## Requirements
Django==6.0.6
pillow==12.2.0
qrcode==8.2

Full list in `requirements.txt`.

---

## Environment Variables (Production)

For production, move these out of `settings.py` into environment variables:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Set to `False` in production |


---

## Admin Panel

Visit **http://127.0.0.1:8000/admin** after creating a superuser to manage
all users, short URLs, and click records directly.

---

## License

MIT — free to use and modify.