# Grovia - Plant Disease Detection System

A modern web application for detecting plant diseases using AI-powered image analysis. Built with Vue.js frontend and FastAPI backend, featuring Google Gemini Vision API for accurate disease identification.

## Features

- **AI-Powered Detection**: Accurate plant disease identification using Google Gemini Vision API
- **Leaf Validation**: Pre-filters non-plant images to ensure valid inputs
- **User Authentication**: Secure JWT-based authentication with Google OAuth support
- **Detection History**: Track and review past disease detections
- **Cloud Storage**: Image storage via Cloudinary
- **Responsive Design**: Mobile-friendly interface

## Tech Stack

**Frontend:**
- Vue.js 3 with Composition API
- Vite for fast development
- Pinia for state management
- Vue Router for navigation

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy ORM
- MySQL/MariaDB database
- Alembic for migrations
- Google Gemini AI
- OpenCV for image validation

## Project Structure

```
grovia/
├── grovia-backend/     # FastAPI Backend + ML Model
├── grovia-frontend/    # Vue.js Frontend
└── README.md           # File ini
```

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- MySQL/MariaDB 10.4+
- Git

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/ravillust/grovia.git
cd grovia
```

### 2. Backend Setup

```bash
cd grovia-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (see Configuration section)
cp .env.example .env

# Run database migrations
alembic upgrade head
```

### 3. Frontend Setup

```bash
cd grovia-frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
```

### 4. Database Setup

Create a MySQL database:

```sql
CREATE DATABASE grovia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Configuration

### Backend Environment Variables

Create `.env` in `grovia-backend/` directory:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/grovia_db

# Security
SECRET_KEY=your-secret-key-min-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# Email Configuration (for password reset)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Cloud Storage (optional)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
USE_CLOUDINARY=true
```

**Get API Keys:**
- Gemini AI: https://makersuite.google.com/app/apikey
- Google OAuth: https://console.cloud.google.com/
- Cloudinary: https://cloudinary.com/

### Frontend Environment Variables

Create `.env` in `grovia-frontend/` directory:

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_GOOGLE_CLIENT_ID=your-google-client-id
```

## Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd grovia-backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd grovia-frontend
npm run dev
```

Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Production Build

**Backend:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**
```bash
npm run build
# Deploy dist/ folder to hosting service
```

## API Documentation

After starting the backend server:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health-check

## Database Schema

The application uses two main tables:

### Users Table
- Authentication and user profile management
- Google OAuth integration support
- Email verification and password reset tokens

### Detection History Table
- Stores plant disease detection results
- Links to user accounts
- Includes image URLs and AI predictions

## Development

### Code Structure

```
grovia-backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core configuration and security
│   ├── crud/         # Database operations
│   ├── ml/           # Machine learning models
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   └── utils/        # Utility functions
├── alembic/          # Database migrations
└── uploads/          # Temporary file storage

grovia-frontend/
├── src/
│   ├── components/   # Vue components
│   ├── views/        # Page views
│   ├── router/       # Vue Router configuration
│   ├── stores/       # Pinia state management
│   └── services/     # API service layer
└── public/           # Static assets
```

### Running Tests

```bash
# Backend tests
cd grovia-backend
pytest

# Frontend tests (if available)
cd grovia-frontend
npm run test
```

## Troubleshooting

### Database Connection Issues
- Ensure MySQL/MariaDB is running
- Verify DATABASE_URL in .env
- Check database user permissions

### Gemini API Errors
- Verify GEMINI_API_KEY is correct
- Check API quota limits at Google AI Studio
- Ensure internet connection is stable

### Image Upload Failures
- If using Cloudinary, verify credentials
- Check file size limits (default: 10MB)
- Ensure UPLOAD_DIR has write permissions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Google Gemini AI for disease detection
- FastAPI framework
- Vue.js framework
- OpenCV for image processing

### Frontend
- Modern UI dengan Vue 3 + Vite
- Image Upload & Preview
- Real-time Detection
- History Management
- Responsive Design
- Authentication Flow

## Development Commands

### Backend

```cmd
cd grovia-backend

REM Activate virtual environment
venv\Scripts\activate.bat

REM Run server
uvicorn app.main:app --reload

REM Run migration
alembic upgrade head

REM Create new migration
alembic revision --autogenerate -m "description"
```

### Frontend

```cmd
cd grovia-frontend

REM Install dependencies
npm install

REM Run dev server
npm run dev

REM Build for production
npm run build

REM Preview production build
npm run preview
```

## Dependencies

### Backend
- FastAPI 0.109.2
- Uvicorn 0.27.1
- SQLAlchemy 2.0.25
- MySQL Client
- Google Generative AI 0.3.2
- Cloudinary 1.36.0
- Python-Jose (JWT)
- Pillow, OpenCV (Image processing)

### Frontend
- Vue 3.4.21
- Vue Router 4.3.0
- Pinia 2.1.7 (State Management)
- Axios 1.6.7
- Vite 5.1.5
- Lucide Icons

## Troubleshooting

### Port sudah digunakan

**Backend (port 8000):**
```cmd
REM Cari proses yang menggunakan port
netstat -ano | findstr :8000

REM Kill proses (ganti PID dengan ID yang ditemukan)
taskkill /PID <PID> /F
```

**Frontend (port 5173):**
```cmd
REM Cari proses yang menggunakan port
netstat -ano | findstr :5173

REM Kill proses
taskkill /PID <PID> /F
```

### Virtual Environment Error

```cmd
cd grovia-backend
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Node Modules Error

```cmd
cd grovia-frontend
rmdir /s /q node_modules
del package-lock.json
npm install
```

### Database Connection Error

1. Pastikan MySQL/MariaDB running
2. Cek kredensial di `.env`
3. Pastikan database `grovia_db` sudah dibuat
4. Test connection:

```cmd
mysql -u root -p
USE grovia_db;
SHOW TABLES;
```

## Testing

### Test Backend

```cmd
cd grovia-backend
venv\Scripts\activate.bat

REM Test basic functionality
python check_uploads.py

REM Test dengan curl
curl http://localhost:8000/api/v1/health-check
```

### Test Frontend

```cmd
cd grovia-frontend
npm run dev
```

Buka browser: http://localhost:5173

## Production Deployment

### Backend (Railway/Render/DigitalOcean)

```cmd
cd grovia-backend

REM Pastikan semua environment variables ter-set
REM Update ALLOWED_ORIGINS di .env dengan production URL

uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend (Vercel/Netlify)

```cmd
cd grovia-frontend

REM Update VITE_API_URL di .env dengan production backend URL
npm run build

REM Deploy folder dist/
```

## Support

Untuk masalah atau pertanyaan:
1. Cek dokumentasi di `grovia-backend/README.md`
2. Cek logs di `grovia-backend/logs/app.log`
3. Test API di http://localhost:8000/docs

## License

Educational Project - Grovia Team

---

Last Updated: November 18, 2025
