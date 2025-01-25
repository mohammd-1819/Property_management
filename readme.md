# Property Management System API

This project is a comprehensive **Property Management System API**, allowing users to list their properties for sale, manage transactions, and book property viewings. Built with Django REST Framework (DRF), it offers a robust and scalable platform for managing real estate operations. The project is fully dockerized and uses Redis for caching data to enhance performance.

## Prerequisites

Before setting up the project, ensure that you have the following installed:

- Docker and Docker Compose
- Python 3.11
- Django 5.1 or higher
- Django REST Framework
- PostgreSQL
- Redis
- Virtualenv (optional but recommended)

## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohammd-1819/Property_management.git
   cd Property_management
   ```

2. **Create and activate a virtual environment (optional if not using Docker):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database:**
   - Update the `DATABASES` section in `settings/local.py` with your PostgreSQL credentials.

5. **Set up Redis:**
   - Ensure Redis is running locally or through Docker.
   - Update the caching configuration in `settings/base.py` to use Redis.

6. **Apply the migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser for the admin panel (optional but recommended):**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server (if not using Docker):**
   ```bash
   python manage.py runserver
   ```

9. **Using Docker:**
   - Build and run the Docker containers:
     ```bash
     docker-compose up --build
     ```
   - The application will be accessible at [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/).

## Features

- **User Management:**
  - User registration and authentication using JWT tokens.
  - Property owners can list and manage their properties.


- **Property Listings:**
  - Create, view, edit, and delete property listings.


- **Booking System:**
  - Users can request property viewings.
  - Admins can manage and approve bookings.


- **Transactions:**
  - Track and manage property sales.


- **Caching:**
  - Redis is used to cache frequently accessed data, improving performance.


- **Admin Panel:**
  - Manage users, properties, and bookings.

## API Endpoints

- **Authentication:**
  - Register, and obtain JWT tokens.


- **Properties:**
  - Create, update, view, and delete property listings.


- **Bookings:**
  - Request property viewings.
  - Manage booking requests.


- **Transactions:**
  - Manage and track property sales.


## Technologies Used

- **Backend:** Django REST Framework
- **Database:** PostgreSQL
- **Caching:** Redis
- **Containerization:** Docker
- **Authentication:** JWT-based authentication system

## Authors

Developed by Mohammad Charipour
