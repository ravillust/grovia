# GROVIA - Plant Disease Detection System

Aplikasi deteksi penyakit tanaman menggunakan AI (Gemini Vision API) dengan frontend Vue.js dan backend FastAPI.

## Struktur Proyek

```
grovia/
├── grovia-backend/     # FastAPI Backend + ML Model
├── grovia-frontend/    # Vue.js Frontend
└── README.md           # File ini
```

## Quick Start

### 1. First Time Setup

Install dependencies secara manual:

**Backend:**
```cmd
cd grovia-backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

**Frontend:**
```cmd
cd grovia-frontend
npm install
```

### 2. Pastikan Database Running

Gunakan Laragon atau XAMPP:
- Start MySQL/MariaDB service
- Buat database baru bernama `grovia_db`:

```sql
CREATE DATABASE grovia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Jalankan Development Server

**Terminal 1 - Backend:**
```cmd
cd grovia-backend
venv\Scripts\activate.bat
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```cmd
cd grovia-frontend
npm run dev
```

Server akan berjalan di:
- Backend: http://localhost:8000
- Frontend: http://localhost:5173

## Konfigurasi

### Backend (.env)

File: `grovia-backend/.env`

```env
# Database
DATABASE_URL=mysql+pymysql://root@localhost:3306/grovia_db

# Security
SECRET_KEY=your-secret-key-here

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# Cloudinary (Optional)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
USE_CLOUDINARY=true
```

### Frontend (.env)

File: `grovia-frontend/.env`

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## API Documentation

Setelah backend berjalan, akses dokumentasi interaktif:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/api/v1/health-check

## Fitur Utama

### Backend
- Authentication (JWT-based)
- Plant Disease Detection dengan Gemini AI
- Leaf Image Validator
- RAG Knowledge Base (10 penyakit tanaman)
- Detection History
- Cloudinary Integration (image storage)
- MySQL Database

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
