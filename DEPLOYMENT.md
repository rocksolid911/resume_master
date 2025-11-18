# Deployment Guide

This guide covers deploying the AI Resume Builder application to production.

## Table of Contents

1. [Backend Deployment](#backend-deployment)
2. [Frontend Deployment](#frontend-deployment)
3. [Database Setup](#database-setup)
4. [Environment Variables](#environment-variables)
5. [SSL/HTTPS Configuration](#ssl-https-configuration)
6. [Monitoring & Logging](#monitoring--logging)

## Backend Deployment

### Option 1: Heroku

1. **Prerequisites**:
   - Heroku CLI installed
   - Git repository initialized

2. **Create Heroku App**:
   ```bash
   heroku create resume-builder-api
   ```

3. **Add Buildpacks**:
   ```bash
   heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
   heroku buildpacks:add --index 2 heroku/python
   ```

4. **Provision PostgreSQL**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

5. **Set Environment Variables**:
   ```bash
   heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=resume-builder-api.herokuapp.com
   heroku config:set OPENAI_API_KEY=your-openai-api-key
   heroku config:set CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

6. **Deploy**:
   ```bash
   cd backend
   git push heroku main
   ```

7. **Run Migrations**:
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py seed_templates
   ```

### Option 2: AWS EC2

1. **Launch EC2 Instance**:
   - Ubuntu 22.04 LTS
   - t2.medium or larger
   - Security group: Allow ports 22, 80, 443

2. **SSH into Instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Dependencies**:
   ```bash
   sudo apt update
   sudo apt install -y python3.11 python3-pip postgresql nginx
   ```

4. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/resume-builder.git
   cd resume-builder/backend
   ```

5. **Setup Virtual Environment**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Configure Nginx**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static/ {
           alias /path/to/backend/staticfiles/;
       }

       location /media/ {
           alias /path/to/backend/media/;
       }
   }
   ```

7. **Setup Systemd Service**:
   ```ini
   [Unit]
   Description=Resume Builder API
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/resume-builder/backend
   ExecStart=/home/ubuntu/resume-builder/backend/venv/bin/gunicorn resume_builder.wsgi:application --bind 0.0.0.0:8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

### Option 3: DigitalOcean App Platform

1. **Create App**:
   - Connect GitHub repository
   - Select backend directory as source

2. **Configure**:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Run Command: `gunicorn resume_builder.wsgi:application --bind 0.0.0.0:$PORT`

3. **Add Database**:
   - Add managed PostgreSQL database

4. **Set Environment Variables** in App Platform dashboard

## Frontend Deployment

### Option 1: Vercel (Web)

1. **Build for Production**:
   ```bash
   cd frontend
   flutter build web --release
   ```

2. **Deploy**:
   ```bash
   cd build/web
   vercel deploy --prod
   ```

3. **Configure Environment**:
   - Set `API_URL` in Vercel environment variables

### Option 2: Firebase Hosting (Web)

1. **Install Firebase CLI**:
   ```bash
   npm install -g firebase-tools
   ```

2. **Initialize Firebase**:
   ```bash
   firebase init hosting
   ```

3. **Build and Deploy**:
   ```bash
   flutter build web --release
   firebase deploy --only hosting
   ```

### Option 3: Mobile App Stores

**iOS (App Store)**:

1. **Build**:
   ```bash
   flutter build ios --release
   ```

2. **Open Xcode**:
   ```bash
   open ios/Runner.xcworkspace
   ```

3. **Archive and Upload**:
   - Product > Archive
   - Distribute App
   - Upload to App Store Connect

**Android (Play Store)**:

1. **Generate Signing Key**:
   ```bash
   keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
   ```

2. **Configure Gradle**:
   Edit `android/key.properties`:
   ```
   storePassword=<password>
   keyPassword=<password>
   keyAlias=upload
   storeFile=<path-to-keystore>
   ```

3. **Build APK/Bundle**:
   ```bash
   flutter build appbundle --release
   ```

4. **Upload to Play Console**

## Database Setup

### PostgreSQL Configuration

1. **Production Database**:
   ```sql
   CREATE DATABASE resume_builder_prod;
   CREATE USER resume_builder_user WITH PASSWORD 'strong-password';
   GRANT ALL PRIVILEGES ON DATABASE resume_builder_prod TO resume_builder_user;
   ```

2. **Connection String**:
   ```
   postgresql://resume_builder_user:strong-password@localhost:5432/resume_builder_prod
   ```

3. **Backup Strategy**:
   ```bash
   # Daily backup
   pg_dump resume_builder_prod > backup_$(date +%Y%m%d).sql

   # Restore
   psql resume_builder_prod < backup_20240101.sql
   ```

## Environment Variables

### Backend (.env)

```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=api.yourdomain.com,yourdomain.com

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# OpenAI
OPENAI_API_KEY=sk-your-api-key

# AWS S3 (Optional)
USE_S3=True
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# JWT
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# Rate Limiting
AI_ENHANCEMENT_RATE_LIMIT=5
```

### Frontend

Update `lib/config/api_config.dart`:
```dart
static const String baseUrl = 'https://api.yourdomain.com';
```

## SSL/HTTPS Configuration

### Let's Encrypt (Free SSL)

1. **Install Certbot**:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Obtain Certificate**:
   ```bash
   sudo certbot --nginx -d api.yourdomain.com
   ```

3. **Auto-Renewal**:
   ```bash
   sudo certbot renew --dry-run
   ```

## Monitoring & Logging

### Backend Monitoring

1. **Install Sentry** (Error Tracking):
   ```bash
   pip install sentry-sdk
   ```

   Configure in `settings.py`:
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.django import DjangoIntegration

   sentry_sdk.init(
       dsn="your-sentry-dsn",
       integrations=[DjangoIntegration()],
       traces_sample_rate=1.0,
   )
   ```

2. **Application Performance Monitoring**:
   - Use Django Debug Toolbar (development)
   - New Relic or Datadog (production)

### Logging

Configure in `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/resume_builder/app.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Performance Optimization

### Backend

1. **Enable Caching**:
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

2. **Database Optimization**:
   - Add indexes to frequently queried fields
   - Use select_related() and prefetch_related()
   - Enable connection pooling

3. **Static Files**:
   - Use WhiteNoise for static file serving
   - Configure CDN for media files (CloudFront, CloudFlare)

### Frontend

1. **Code Splitting**: Already handled by Flutter web build

2. **Asset Optimization**:
   - Compress images
   - Use appropriate image formats (WebP)

3. **Lazy Loading**: Implement for lists and images

## Security Checklist

- [ ] HTTPS enabled on all domains
- [ ] Environment variables secured
- [ ] Database credentials rotated
- [ ] Firewall rules configured
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation on all forms
- [ ] SQL injection protection (ORM usage)
- [ ] XSS protection enabled
- [ ] CSRF tokens configured
- [ ] Regular security updates
- [ ] Backup strategy implemented
- [ ] Monitoring and alerting setup

## Troubleshooting

### Common Issues

1. **Database Connection Failed**:
   - Check DATABASE_URL format
   - Verify PostgreSQL is running
   - Check firewall rules

2. **Static Files Not Loading**:
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT and STATIC_URL settings

3. **CORS Errors**:
   - Verify CORS_ALLOWED_ORIGINS includes frontend domain
   - Check allowed methods and headers

4. **AI Enhancement Failing**:
   - Verify OPENAI_API_KEY is set
   - Check API rate limits
   - Review error logs

## Maintenance

### Regular Tasks

- **Daily**: Monitor error logs and performance
- **Weekly**: Review and rotate logs
- **Monthly**: Update dependencies, security patches
- **Quarterly**: Database backup restoration test
- **Annually**: SSL certificate renewal, security audit

---

For additional support, consult the main README.md or contact the development team.
