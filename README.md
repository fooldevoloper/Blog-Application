
# Full Stack Blog App - Monorepo Architecture

This repository contains the architectural plan for a Full Stack Blog App using Django (backend) and Next.js (frontend) 

## Project Structure

```
blog-app-monorepo/
├── backend/                 # Django backend (60%)
├── frontend/                # Next.js frontend (40%)
├── docs/                    # Documentation
├── README.md
└── .gitignore
```

## Documentation

1. [Monorepo Architecture](https://chatgpt.com/c/monorepo-architecture.md) - Complete architecture plan
2. [Backend Details](https://chatgpt.com/c/backend-details.md) - Detailed Django backend structure
3. [Frontend Details](https://chatgpt.com/c/frontend-details.md) - Detailed Next.js frontend structure
4. [Environment Variables](https://chatgpt.com/c/environment-variables.md) - Environment variable specifications
5. [Setup Commands](https://chatgpt.com/c/setup-commands.md) - Detailed setup instructions
6. [Final Architecture Summary](https://chatgpt.com/c/final-architecture-summary.md) - Consolidated overview

## Backend (Django) - 60% Weight

### Key Features

* Django REST API without DRF
* JWT authentication with pyjwt (1-hour expiry)
* Custom logging middleware
* SQLite database (configurable)
* Proper error handling (401, 403, 404)

### API Endpoints

* POST /register/ - User registration
* POST /login/ - JWT token generation
* GET /posts/ - List all posts
* GET /posts/`<id>`/ - Get post details
* POST /posts/ - Create new post (authenticated)
* PUT /posts/`<id>`/ - Update post (author only)
* DELETE /posts/`<id>`/ - Delete post (author only)

## Frontend (Next.js) - 40% Weight

### Key Features

* Next.js 13+ with App Router
* Tailwind CSS for styling
* State management with Redux Toolkit or Zustand
* Axios for API requests
* Responsive design
* Protected routes

### Pages

* Home (posts list)
* Login/Registration
* Post detail
* Create/Edit post
* User profile

## Getting Started

Refer to [Setup Commands](https://chatgpt.com/c/setup-commands.md) for detailed installation instructions.

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

### Seeder (Sample Data)

We have included a `seeder.py` script to quickly populate the database with **sample users** and  **posts** .

#### Run Seeder

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python seeder.py
```

#### Test Credentials (from `seeder.py`)

| Username   | Email                                    | Password    |
| ---------- | ---------------------------------------- | ----------- |
| john_doe   | [john@example.com](mailto:john@example.com) | password123 |
| jane_smith | [jane@example.com](mailto:jane@example.com) | password123 |
| bob_wilson | [bob@example.com](mailto:bob@example.com)   | password123 |

These users come with sample posts to help you test the API quickly.

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Environment Variables

See [Environment Variables](https://chatgpt.com/c/environment-variables.md) for detailed specifications.

### Backend (.env.example)

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA=3600
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env.example)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Blog App
```

## Development Workflow

1. Start backend server: `cd backend && python manage.py runserver`
2. Start frontend server: `cd frontend && npm run dev`
3. Access application at [http://localhost:3000](http://localhost:3000/)

## Deployment Considerations

* Use PostgreSQL for production database
* Set DEBUG=False in production
* Use environment variables for secrets
* Implement proper logging
* Set up CORS properly for production
* Use HTTPS in production

## Dependencies

### Backend (requirements.txt)

```
Django>=4.2,<5.0
pyjwt>=2.8.0
python-decouple>=3.8
django-cors-headers>=4.3.0
```

### Frontend (package.json)

```json
{
  "dependencies": {
    "next": "latest",
    "react": "latest",
    "react-dom": "latest",
    "axios": "^1.6.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "zustand": "^4.4.0",
    "@reduxjs/toolkit": "^1.9.0",
    "react-redux": "^8.1.0",
    "react-icons": "^4.10.0"
  }
}
```
