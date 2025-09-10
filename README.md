# Nail Art Shop

A Django-based ### Deployment Steps
1. Push your code to GitHub
2. In Render dashboard, create a new Web Service
3. Connect your GitHub repository
4. Configure the service:
   - **Runtime**: Python 3 (or specify python-3.11 in runtime.txt)
   - **Build Command**: `chmod +x build.sh && ./build.sh` (uses the build script for better error handling)
   - **Start Command**: `gunicorn nailshop.wsgi:application --bind 0.0.0.0:$PORT`
5. Set environment variables:
   - `DEBUG=False`
   - `SECRET_KEY` (generate a new random key)
   - `ALLOWED_HOSTS` (your Render app URL, e.g., `your-app.onrender.com`)
6. The PostgreSQL database will be automatically created
7. Deploy the application

### Troubleshooting
- If you encounter Pillow build errors, ensure you're using Pillow>=10.2.0
- For Python 3.13 compatibility issues, you can specify Python 3.11 in `runtime.txt`
- Make sure to use `requirements-prod.txt` for production deploymentlication for nail art products.

## Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your local settings
6. Run migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Run the development server: `python manage.py runserver`

## Deployment to Render

### Prerequisites
1. Create a Render account and connect your GitHub repository
2. For PostgreSQL support in production, you may need to install system dependencies. Render handles this automatically.

### Production Requirements
Before deploying, update your `requirements.txt` to include PostgreSQL support:

```txt
Django==4.2.0
Pillow>=10.2.0
psycopg2-binary>=2.9.9
gunicorn==21.2.0
whitenoise==6.6.0
```

**Note**: Pillow version >=10.2.0 is required for compatibility with Python 3.13 on Render.

### Deployment Steps
1. Push your code to GitHub
2. In Render dashboard, create a new Web Service
3. Connect your GitHub repository
4. Configure the service:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn nailshop.wsgi:application --bind 0.0.0.0:$PORT`
5. Set environment variables:
   - `DEBUG=False`
   - `SECRET_KEY` (generate a new random key)
   - `ALLOWED_HOSTS` (your Render app URL, e.g., `your-app.onrender.com`)
6. The PostgreSQL database will be automatically created
7. Deploy the application

### Media Files in Production

For production deployment, it's recommended to use a cloud storage service like AWS S3, Cloudinary, or Google Cloud Storage for media files instead of storing them locally. This is because:

- Render's file system is ephemeral
- Better performance and scalability
- Cost-effective storage

To implement cloud storage, you can use django-storages with boto3 for S3:

```bash
pip install django-storages boto3
```

Then configure in settings.py:
```python
# settings.py
INSTALLED_APPS += ['storages']

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

## Features

- Product catalog with categories
- Shopping cart functionality
- User authentication and profiles
- Order management
- Payment method tracking
- Contact form
- Responsive design

## Technologies Used

- Django 4.2
- PostgreSQL
- Pillow (for image handling)
- WhiteNoise (for static files)
- Gunicorn (WSGI server)
