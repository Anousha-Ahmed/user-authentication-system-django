# 🔐 User Authentication System

A complete production-ready user authentication and student management REST API built with Django REST Framework, featuring email OTP verification, session-based authentication, and full CRUD operations with pagination.

## ✨ Features

**User Authentication**
- Registration with email OTP verification
- Session-based login/logout
- Forgot password with OTP
- Password reset & update
- Session status check

**Student Management**
- List students with pagination (10-100 per page)
- Create, read, update, delete students
- Unique roll number validation

**Email Service**
- OTP generation (6-digit)
- OTP resend functionality
- SMTP integration with Gmail

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Django 5.x |
| API | Django REST Framework |
| Authentication | Session-based |
| Database | SQLite3 |
| Email | Gmail SMTP |
| Pagination | Django Paginator |

## 🚀 Quick Start

```bash
# Clone and enter directory
cd USERAUTHENTICATIONSYSTEM

# Activate virtual environment
env\Scripts\activate          # Windows
source env/bin/activate       # Mac/Linux

# Install dependencies
pip install django djangorestframework django-cors-headers python-dotenv

# Configure environment variables
# Create .env file with:
# EMAIL_HOST_USER=your_email@gmail.com
# EMAIL_HOST_PASSWORD=your_app_password
# SECRET_KEY=your_secret_key
# DEBUG=True

# Run migrations
python manage.py makemigrations users
python manage.py migrate

# Start server
python manage.py runserver