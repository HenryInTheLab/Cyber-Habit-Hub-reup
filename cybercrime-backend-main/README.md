# Backend

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the project root with the following variables for local development:

```
SAFE_BROWSING_API_KEY=your-google-safe-browsing-api-key
SECRET_KEY=your-django-secret-key
DJANGO_DEBUG=True
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PWD=your-db-password
DB_HOST=your-db-host
DB_PORT=5432
```

### 2. Build and Run with Docker

```bash
docker-compose up --build
```

This will build the Docker image and start the backend server.

### 3. Automatic Deployment

Any push to the `main` branch will trigger an automatic deployment to the EC2 server via GitHub Actions.

### 4. API Documentation

The deployed backend API documentation is available at:

```
https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/
```