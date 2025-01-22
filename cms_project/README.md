# Django CMS API

A Content Management System API built with Django Rest Framework.

## Features

- User authentication (Admin and Author roles)
- Content management with CRUD operations
- Role-based permissions
- Content search functionality
- Test coverage reports

## Setup Instructions

1. Clone the repository
2. Create virtual environment: python -m venv venv
3. Activate virtual environment:
   - Windows: venv\Scripts\activate
   - Unix: source venv/bin/activate
4. Install dependencies: pip install -r requirements.txt
5. Run migrations: python manage.py migrate
6. Create superuser: python manage.py createsuperuser
7. Run tests: python manage.py test
8. Start server: python manage.py runserver

## API Endpoints

### Authentication
- POST /api/auth/register/ - Author registration
- POST /api/auth/login/ - User login

### Content Management
- GET /api/content/ - List contents
- POST /api/content/ - Create content
- GET /api/content/{id}/ - Retrieve content
- PUT /api/content/{id}/ - Update content
- DELETE /api/content/{id}/ - Delete content
- GET /api/content/search/ - Search contents

## Running Tests

bash
coverage run manage.py test
coverage report
coverage html  # Generates HTML report
![Screenshot 2025-01-22 132516](https://github.com/user-attachments/assets/e14b171f-0e85-4f9f-a331-6c6dacb1c07c)
