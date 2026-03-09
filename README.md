# Event Management API

## Project Overview

The **Event Management API** is a backend system built with **Django** and **Django REST Framework (DRF)** that allows organizers to create and manage events while enabling attendees to register, cancel registrations, and join waitlists when events reach maximum capacity.

The API implements **JWT authentication**, **role-based access control**, **event capacity enforcement**, **pagination**, and **filtering**.

This project demonstrates backend API design, authentication, database management, and RESTful architecture.

---

# Features

### Authentication

* JWT-based authentication using **SimpleJWT**
* Secure login and token generation
* Protected API endpoints

### User Roles

Two user roles are supported:

* **Organizer**

  * Create events
  * Manage event details

* **Attendee**

  * Register for events
  * Cancel registration
  * Join waitlist if event capacity is reached

### Event Management

Organizers can:

* Create new events
* Define event title, location, date, and maximum capacity

### Event Registration

Attendees can:

* Register for events
* Cancel registration
* Automatically join a waitlist when an event is full

### Waitlist System

If event capacity is reached:

* New registrations are placed on a waitlist
* When a registered attendee cancels, the first waitlisted attendee is promoted

### Filtering & Pagination

The API supports:

* Event filtering
* Pagination for event lists

---

# Technology Stack

* **Backend Framework:** Django 5
* **API Framework:** Django REST Framework
* **Authentication:** JWT (SimpleJWT)
* **Database:** SQLite3
* **Deployment:** Render
* **Testing Tool:** Postman
* **Static Files:** WhiteNoise

---

# Project Structure

```
event_management/
│
├── accounts/                # Custom user management
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── events/                  # Event management logic
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── event_management/        # Main project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── db.sqlite3
```

---

# Database Configuration

This project uses **SQLite3** for development and deployment.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

SQLite was chosen because it is lightweight and easy to deploy without requiring external database services.

---

# Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/event-management-api.git
cd event-management-api
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

---

## 6. Run Development Server

```bash
python manage.py runserver
```

Server will start at:

```
http://127.0.0.1:8000/
```

---

# API Endpoints

## Authentication

### Login

```
POST /api/token/
```

Request Body:

```json
{
  "username": "organizer1",
  "password": "Luminous123!"
}
```

Response:

```json
{
  "refresh": "token",
  "access": "token"
}
```

---

# Event Endpoints

## Create Event

```
POST /api/events/
```

Authorization:

```
Bearer ACCESS_TOKEN
```

Request Body:

```json
{
  "title": "Backend Masterclass",
  "location": "Lagos",
  "date": "2026-03-20",
  "max_capacity": 50
}
```

---

## View Events

```
GET /api/events/
```

---

## View Upcoming Events

```
GET /api/events/upcoming/
```

---

## Register For Event

```
POST /api/events/{event_id}/register/
```

No request body required.

Authorization required.

---

## Cancel Registration

```
POST /api/events/{event_id}/cancel_registration/
```

---

# Pagination

The API uses **PageNumberPagination**.

Default page size:

```
5 events per page
```

Example:

```
GET /api/events/?page=2
```

---

# Deployment

The project is deployed on **Render**.

### Static Files

WhiteNoise is used to serve static files.

```
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

### Allowed Hosts

```
ALLOWED_HOSTS = ['.onrender.com']
```

---

# Testing

All API endpoints were tested using **Postman**.

Example test flow:

1. Login to obtain JWT token
2. Create an event
3. Register attendee
4. Attempt over-registration
5. Add attendee to waitlist
6. Cancel registration

---

# Security

The API uses:

* JWT authentication
* Django password validation
* Protected endpoints
* Role-based access control

---

# Future Improvements

* Email notifications for registrations
* Event reminders
* Admin analytics dashboard
* Event image uploads
* Search functionality

---

# Author

**Adebayo Ajani Ismail**

Backend Developer
Specializing in Django REST API Development


