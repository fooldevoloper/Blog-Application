# Backend Setup

## Seeding Data

To seed the database with sample data, run:

```bash
python seeder.py
```

This will create:
- One sample user (testuser / test@example.com / password123)
- Three sample blog posts

## Running the Development Server

After seeding data, start the development server:

```bash
python manage.py runserver
```

The API will be available at http://localhost:8000