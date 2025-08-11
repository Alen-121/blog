# Django Blog Application Development & Deployment Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Application Configuration](#application-configuration)
5. [Development Process](#development-process)
6. [Heroku Deployment Process](#heroku-deployment-process)
7. [Post-Deployment Management](#post-deployment-management)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

## Project Overview

### Application Details
- **Project Name**: Blog
- **Framework**: Django 5.2.5
- **Language**: Python
- **Database**: SQLite (Development), PostgreSQL (Production)
- **Deployment Platform**: Heroku
- **Live URL**: https://alen-django-blog-5828ae733c9a.herokuapp.com/

### Key Features
- Django REST Framework integration
- User authentication system
- Blog application functionality
- API documentation with drf-yasg (Swagger)
- Custom user model
- Responsive design templates

### Applications Structure
- `blog_application/` - Main blog functionality
- `user_auth/` - Custom user authentication
- Django admin interface
- REST API endpoints

## Development Environment Setup

### Prerequisites
- Python 3.11+
- Git
- Virtual environment (venv)
- Code editor (VS Code, PyCharm, etc.)

### Initial Setup Commands
```bash
# Create project directory
mkdir Blog
cd Blog

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install Django and dependencies
pip install django djangorestframework drf-yasg python-decouple

# Create Django project
django-admin startproject Blog .

# Create applications
python manage.py startapp blog_application
python manage.py startapp user_auth
```

## Project Structure

```
Blog/
├── Blog/                    # Main project directory
│   ├── __init__.py
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── blog_application/       # Blog app
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── user_auth/             # Authentication app
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   └── ...
├── venv/                  # Virtual environment
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku process file
├── runtime.txt          # Python version specification
├── .gitignore          # Git ignore rules
└── db.sqlite3          # Development database
```

## Application Configuration

### Key Dependencies
```txt
asgiref==3.9.1
Django==5.2.5
djangorestframework==3.16.1
drf-yasg==1.21.10
gunicorn==23.0.0
inflection==0.5.1
packaging==25.0
python-decouple==3.8
pytz==2025.2
PyYAML==6.0.2
sqlparse==0.5.3
uritemplate==4.2.0
whitenoise==6.9.0
dj-database-url
psycopg2-binary
```

### Settings Configuration (settings.py)

#### Installed Apps
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog_application',
    'user_auth',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
]
```

#### Middleware Configuration
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

#### Database Configuration
```python
import os
import dj_database_url

# Development vs Production database
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

#### Environment Variables
```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = ['*']  # Configure appropriately for production
```

#### Static Files Configuration
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### REST Framework Settings
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5
}
```

#### Custom User Model
```python
AUTH_USER_MODEL = 'user_auth.UserData'
```

## Development Process

### 1. Local Development Workflow
```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### 2. Git Version Control Setup
```bash
# Initialize Git repository
git init

# Create .gitignore file
cat > .gitignore << 'EOF'
# Django
*.log
*.pot
*.pyc
__pycache__/
db.sqlite3
db.sqlite3-journal
media/

# Environment variables
.env
.venv
venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Static files
staticfiles/
EOF

# Add and commit files
git add .
git commit -m "Initial Django project setup"
```

## Heroku Deployment Process

### 1. Prerequisites
- Heroku account (verified with payment method)
- Heroku CLI installed
- Git repository with your project

### 2. Heroku CLI Installation
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu/Debian
sudo snap install --classic heroku

# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

### 3. Authentication
```bash
heroku login
```

### 4. Deployment Configuration Files

#### Procfile
```
web: gunicorn Blog.wsgi --log-file -
```

#### runtime.txt
```
python-3.11.5
```

#### requirements.txt
```bash
pip freeze > requirements.txt
```

### 5. Deployment Steps
```bash
# Create Heroku application
heroku create alen-django-blog

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False

# Deploy application
git push heroku main

# Run database migrations
heroku run python manage.py migrate

# Collect static files
heroku run python manage.py collectstatic --noinput

# Create superuser (optional)
heroku run python manage.py createsuperuser

# Open deployed application
heroku open
```

### 6. Environment Variables Management
```bash
# View all config variables
heroku config

# Set individual variables
heroku config:set VARIABLE_NAME="value"

# Remove variables
heroku config:unset VARIABLE_NAME
```

## Post-Deployment Management

### 1. Monitoring and Logs
```bash
# View real-time logs
heroku logs --tail

# View specific number of log lines
heroku logs -n 100

# View app information
heroku info

# Check dyno status
heroku ps
```

### 2. Database Management
```bash
# Run migrations
heroku run python manage.py migrate

# Access Django shell
heroku run python manage.py shell

# Create database backup
heroku pg:backups:capture

# Download database backup
heroku pg:backups:download
```

### 3. Application Management
```bash
# Restart application
heroku restart

# Scale dynos
heroku ps:scale web=1

# Run one-off processes
heroku run python manage.py custom_command
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Module Not Found Error
**Error**: `ModuleNotFoundError: No module named 'dj_database_url'`

**Solution**:
```bash
pip install dj-database-url psycopg2-binary
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add missing dependencies"
git push heroku main
```

#### 2. Static Files Issues
**Error**: Unable to generate Django static files

**Solutions**:
```bash
# Temporary disable
heroku config:set DISABLE_COLLECTSTATIC=1

# Or run manually after deployment
heroku run python manage.py collectstatic --noinput
```

#### 3. Database Connection Issues
**Solution**: Ensure `dj-database-url` is installed and DATABASE_URL is properly configured in settings.

#### 4. Secret Key Issues
**Solution**: 
```bash
heroku config:set SECRET_KEY='your-secret-key-here'
```

### 5. Debug Mode in Production
**Error**: Debug should be False in production

**Solution**:
```bash
heroku config:set DEBUG=False
```

## Best Practices

### 1. Security
- Never commit secret keys to version control
- Use environment variables for sensitive data
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` appropriately
- Use HTTPS in production

### 2. Database
- Regular backups in production
- Use PostgreSQL for production (provided by Heroku)
- Run migrations before deploying new code

### 3. Static Files
- Use WhiteNoise for serving static files
- Configure static file settings properly
- Run `collectstatic` after deployment

### 4. Environment Management
- Use separate settings for development/production
- Utilize environment variables effectively
- Maintain requirements.txt updated

### 5. Monitoring
- Regularly check application logs
- Monitor dyno usage and performance
- Set up error tracking (e.g., Sentry)

### 6. Git Workflow
- Use meaningful commit messages
- Create branches for new features
- Test locally before deploying
- Keep .gitignore updated

### 7. Deployment
- Test in staging environment first
- Deploy during low-traffic periods
- Have rollback plan ready
- Monitor after deployment

## Useful Commands Reference

### Development Commands
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt

# Run development server
python manage.py runserver

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Heroku Commands
```bash
# Login and create app
heroku login
heroku create app-name

# Deploy
git push heroku main

# Environment variables
heroku config
heroku config:set KEY=value

# Database and migrations
heroku run python manage.py migrate
heroku run python manage.py shell

# Logs and monitoring
heroku logs --tail
heroku ps
heroku info

# Open application
heroku open
```

### Git Commands
```bash
# Initialize and add files
git init
git add .
git commit -m "message"

# Push to Heroku
git push heroku main

# Check status
git status
git log --oneline
```

## Conclusion

This documentation provides a comprehensive guide for developing and deploying Django applications to Heroku. Following these practices ensures a smooth development workflow and successful production deployment.

For additional support:
- [Django Documentation](https://docs.djangoproject.com/)
- [Heroku Django Guide](https://devcenter.heroku.com/articles/django-app-configuration)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)

---

**Application URL**: https://alen-django-blog-5828ae733c9a.herokuapp.com/  
**Created**: August 2025  
**Last Updated**: August 11, 2025