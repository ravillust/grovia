# Grovia Backend - Plant Disease Detection API

FastAPI-based backend service for plant disease detection using Google Gemini Vision API with intelligent leaf validation.

## Features

- **Leaf Image Validation**: OpenCV-based pre-filtering to ensure only plant images are processed
- **AI Disease Detection**: Google Gemini 1.5 Flash for accurate disease identification (90%+ accuracy)
- **User Authentication**: JWT-based auth with Google OAuth support
- **Detection History**: Complete tracking of user detection records
- **Cloud Storage**: Cloudinary integration for image management
- **Email Services**: Password reset and verification emails

## Tech Stack

- FastAPI 0.109.2
- SQLAlchemy 2.0.25 (ORM)
- MySQL/MariaDB (Database)
- Alembic (Migrations)
- Google Gemini AI
- OpenCV (Image processing)
- Cloudinary (Cloud storage)
- JWT Authentication

## Getting Started

## Getting Started

### Prerequisites

- Python 3.11+
- MySQL/MariaDB 10.4+
- Google Gemini API Key

### Installation

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

2. **Environment Configuration**

Create `.env` file:

```env
# Database
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/grovia_db

# Security
SECRET_KEY=your-secret-key-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI
GEMINI_API_KEY=your-gemini-api-key

# Email (optional)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

# OAuth (optional)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

# Storage (optional)
USE_CLOUDINARY=true
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

3. **Database Setup**

```bash
# Create database
mysql -u root -p -e "CREATE DATABASE grovia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Run migrations
alembic upgrade head
```

4. **Start Server**

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Server runs at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

```
grovia-backend/
├── app/
│   ├── api/v1/endpoints/      # API endpoints
│   │   ├── auth.py            # Authentication
│   │   ├── detection.py       # Disease detection
│   │   ├── history.py         # Detection history
│   │   └── knowledge.py       # Knowledge base
│   ├── core/                  # Core configs
│   ├── crud/                  # Database operations
│   ├── ml/                    # ML models
│   │   ├── gemini_detector.py # Gemini AI detector
│   │   ├── leaf_validator.py  # Leaf validation
│   │   └── rag_loader.py      # RAG knowledge loader
│   ├── models/                # Database models
│   └── schemas/               # Pydantic schemas
│
├── rag_knowledge/             # Knowledge base (10 diseases)
│   ├── bercak_daun.txt
│   ├── hawar_daun.txt
│   ├── karat_daun.txt
│   ├── busuk_bakteri.txt
│   ├── virus_mozaik.txt
│   ├── defisiensi_nutrisi.txt
│   ├── embun_bulu.txt
│   ├── embun_tepung.txt
│   ├── layu_fusarium.txt
│   └── general_plant_disease.txt
│
├── alembic/                   # Database migrations
├── uploads/                   # User uploaded images
└── requirements.txt           # Python dependencies
```

---

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login user

### Detection
- `POST /api/v1/detection/detect` - Detect disease (requires auth)
- `GET /api/v1/detection/supported-diseases` - List supported diseases

### History
- `GET /api/v1/history/` - Get user's detection history (requires auth)
- `GET /api/v1/history/{id}` - Get specific detection (requires auth)

### Knowledge Base
- `GET /api/v1/knowledge/diseases` - List all diseases
- `GET /api/v1/knowledge/diseases/{id}` - Get disease details

---

## Testing

### Test with cURL

**Register:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'
```

**Detect (with valid leaf image):**
```bash
curl -X POST http://localhost:8000/api/v1/detection/detect \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "image=@path/to/leaf.jpg"
```

---

## Knowledge Base

Sistem memiliki knowledge base untuk 10 penyakit tanaman:

1. **Bercak Daun** (Leaf Spot) - Cercospora spp.
2. **Hawar Daun** (Late Blight) - Phytophthora infestans
3. **Karat Daun** (Rust) - Puccinia spp.
4. **Busuk Bakteri** (Bacterial Rot) - Xanthomonas, Erwinia
5. **Virus Mozaik** (Mosaic Virus) - TMV, CMV, TSWV
6. **Defisiensi Nutrisi** (Nutrient Deficiency)
7. **Embun Bulu** (Downy Mildew)
8. **Embun Tepung** (Powdery Mildew)
9. **Layu Fusarium** (Fusarium Wilt)
10. **General Plant Disease Knowledge**

Setiap knowledge file berisi:
- Penyebab penyakit
- Gejala khas
- Stage perkembangan
- Pengobatan
- Pencegahan
- Diagnosis pembeda

---

## Detection Flow

```
1. User upload foto
   |
2. [Leaf Validator] Cek: Foto daun?
   |- Valid -> Lanjut
   |- Invalid -> Return error + saran
   |
3. [Gemini AI] Analyze image dengan enhanced prompt
   |
4. [RAG Loader] Load knowledge base untuk disease
   |
5. [Enhancement] Gabungkan AI result + RAG knowledge
   |
6. Return comprehensive result:
   - Disease name & confidence
   - AI visual analysis
   - Symptoms observed
   - RAG-enhanced recommendations
   - Prevention tips
   - Detailed symptoms
```

---

## Response Examples

### Valid Leaf Image Response
```json
{
  "success": true,
  "data": {
    "disease_name": "Bercak Daun",
    "confidence_percent": "87%",
    "analysis_method": "Gemini AI Vision + RAG Knowledge",
    "gemini_analysis": "Terdeteksi bercak cokelat dengan tepi kuning...",
    "symptoms_observed": [
      "Bercak cokelat dengan tepi kuning",
      "Diameter bercak 0.5-1.5 cm"
    ],
    "recommendations": [
      "Buang dan bakar daun terinfeksi",
      "Aplikasi fungisida berbahan tembaga"
    ],
    "prevention_tips": [
      "Rotasi tanaman",
      "Jarak tanam yang cukup"
    ],
    "rag_enhanced": true
  }
}
```

### Invalid Image Response
```json
{
  "detail": {
    "error": "invalid_image",
    "message": "FOTO HARUS BERUPA FOTO DAUN/TANAMAN",
    "detected_content": "Terdeteksi wajah manusia",
    "suggestion": "Upload foto daun yang jelas",
    "recommendations": [
      "Upload foto daun tanaman yang jelas",
      "Pastikan fokus pada daun",
      "Gunakan cahaya yang cukup"
    ]
  }
}
```

---

## Configuration

### Environment Variables (.env)
```bash
# Database - MySQL
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/grovia_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# Upload
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=.jpg,.jpeg,.png

# Cloudinary (Optional)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
USE_CLOUDINARY=true
```

---

## Development

### Add New Disease Knowledge

1. Buat file baru di `rag_knowledge/`:
```bash
touch rag_knowledge/penyakit_baru.txt
```

2. Isi dengan format:
```
NAMA PENYAKIT

PENYEBAB:
- Detail penyebab

GEJALA KHAS:
- Gejala 1
- Gejala 2

PENGOBATAN:
- Treatment 1
- Treatment 2

PENCEGAHAN:
- Prevention 1
- Prevention 2
```

3. RAG loader akan auto-detect file baru!

---

## Tech Stack

- **Framework**: FastAPI 0.109.2
- **Server**: Uvicorn 0.27.1
- **Database**: MySQL with SQLAlchemy 2.0.25
- **AI**: Google Generative AI 0.3.2 (Gemini 1.5 Flash)
- **Image Storage**: Cloudinary 1.36.0
- **Authentication**: Python-Jose (JWT)
- **Image Processing**: Pillow, OpenCV

---

## License

Educational Project - Grovia Team

Last Updated: November 18, 2025
