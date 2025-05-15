# Gas Utility Service Management System

A Django application for a gas utility company to manage customer service requests.

## Features

- Customer account management
- Service request submission and tracking
- File attachment support for service requests
- Customer dashboard for viewing request status
- Support staff portal for managing service requests
- Admin functionality for system oversight

## Project Structure

The application is organized into three main Django apps:

1. **customer** - Handles customer account management and profiles
2. **service_requests** - Manages the creation and tracking of service requests
3. **support_portal** - Provides tools for customer support representatives

## Installation

1. Clone the repository
   ```
   git clone https://github.com/iamabhishekch/Gas-Utility-Problem.git
   cd Gas-Utility-Problem
   ```

2. Set up a virtual environment (recommended)
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations
   ```
   python manage.py migrate
   ```

5. Create a superuser
   ```
   python manage.py createsuperuser
   ```

6. Run the development server
   ```
   python manage.py runserver
   ```

## Usage

- Access the customer portal at `/customer/`
- Submit service requests at `/service-requests/create/`
- Support staff can access the portal at `/support/`
- Admin interface is available at `/admin/`

## Technologies Used

- Django
- HTML/CSS/JavaScript
- SQLite (development) / PostgreSQL (production)
