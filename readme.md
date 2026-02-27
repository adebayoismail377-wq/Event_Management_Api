🚀 Event Management API

A powerful RESTful Event Management System built with Django and Django REST Framework, featuring event creation, capacity management, waitlists, filtering, and pagination.

This project demonstrates real-world backend development concepts including secure JWT authentication, relational database management with MySQL, business logic enforcement, and scalable REST API design.

📌 Features

🔐 Authentication & Authorization

User registration

Secure login using JWT (JSON Web Token) Authentication

Access & Refresh token generation

Protected endpoints for authenticated users

Users can only edit or delete events they created


📅 Event Management

Create, update, delete events

Automatic organizer assignment

Public endpoint for viewing upcoming events

🎟 Event Capacity Management

Each event has a maximum capacity

Registration automatically stops when capacity is reached

Users are added to a waitlist if the event is full

Automatic promotion from waitlist when a registered attendee cancels

🔎 Filtering & Search

Users can filter upcoming events by:

Title

Location

Date range

Example:

/api/events/upcoming/?title=backend
/api/events/upcoming/?location=Lagos
/api/events/upcoming/?start_date=2026-03-01&end_date=2026-03-30

📄 Pagination

Upcoming events are paginated

Configurable page size

Navigate pages using:

/api/events/upcoming/?page=2

🛠 Tech Stack

Python 3.11+

Django 5+

Django REST Framework

JWT Authentication (SimpleJWT)

MySQL Database

📂 Project Structure
event_management/
│
├── events/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── event_management/
│   └── settings.py
│
└── manage.py

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/adebayoismail377-wq/event_management_api.git
cd event_management_api
2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run migrations
python manage.py migrate
5️⃣ Start server
python manage.py runserver

Server runs at:

http://127.0.0.1:8000/
🔥 API Endpoints Overview
Method	Endpoint	Description
POST	/api/users/	Register user
GET	/api/events/	List own events
POST	/api/events/	Create event
GET	/api/events/upcoming/	View public upcoming events
POST	/api/events/{id}/register/	Register for event
POST	/api/events/{id}/cancel_registration/	Cancel registration
| POST | /api/token/ | Obtain JWT access & refresh token |
| POST | /api/token/refresh/ | Refresh access token |

🧠 Advanced Logic Implemented

Dynamic seat tracking

Waitlist system

Automatic attendee promotion

Permission-based access control

Query parameter filtering

Paginated API responses

🎯 Project Purpose

This project was built to demonstrate:

Backend API architecture

Business logic implementation

Data integrity enforcement

Scalable event handling

Clean RESTful design principles

It can serve as a foundation for:

Event booking platforms

Conference management systems

Ticketing applications

Community meetup platforms

📈 Future Improvements

Email notifications for waitlist promotion

Payment integration

Admin analytics dashboard

Event image uploads

Docker deployment

👨‍💻 Author

Adebayo Ajani Ismail
Backend Developer | Django Enthusiast