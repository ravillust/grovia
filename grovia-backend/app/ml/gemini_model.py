"""
Gemini AI Model untuk Plant Disease Detection
100% FREE & Powerful AI dari Google
"""
import google.generativeai as genai
from PIL import Image
import os
import logging
from typing import Dict, Optional, List
import json
from pathlib import Path

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

class GeminiPlantDiseaseModel:
    """
    Gemini AI untuk deteksi penyakit tanaman
    Menggunakan Google Gemini Vision API - 100% GRATIS!
    """
    
    def __init__(self):
        """Initialize Gemini AI Model"""
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables!")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Use Gemini 2.5 Flash - latest and fastest multimodal model!
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        logger.info("Gemini AI Plant Disease Model initialized (No RAG)")
        print("Gemini AI Plant Disease Detection ready!")
    
    def create_detection_prompt(self) -> str:
        """
        Create optimized prompt untuk plant disease detection
        dengan kemampuan membedakan penyakit vs defisiensi nutrisi
        """
        prompt = """
        Kamu adalah ahli pertanian dan patologi tanaman profesional dengan keahlian khusus dalam:
        1. Diagnosis penyakit tanaman (jamur, bakteri, virus)
        2. Identifikasi defisiensi nutrisi
        3. Analisis visual gejala pada daun

        Analisis gambar DAUN TANAMAN ini dengan SANGAT TELITI dan identifikasi kondisinya.

        FOKUS ANALISIS PADA DAUN TANAMAN:
        - Pastikan foto adalah daun tanaman (bukan bunga, buah, atau objek lain)
        - Jika foto bukan daun, kembalikan disease_id: "not_a_leaf"

        PENTING - BEDAKAN DENGAN JELAS SEMUA KATEGORI:
        
          A. PENYAKIT INFEKSI JAMUR (Fungal Diseases):
              Ciri khas:
              - Bercak TIDAK MERATA dengan pola tidak teratur
              - Ada zona konsentris (cincin/ring dalam bercak)
              - Bercak memiliki tepi yang JELAS/terpisah dari area sehat
              - Mungkin ada struktur jamur (spora, miselium, fuzz, bubuk)
              - Bercak menyebar dari titik infeksi
              - Warna: coklat tua, hitam, abu-abu, dengan halo kuning
           
              Jenis spesifik:
              * Hawar Daun (Blight - Phytophthora/Alternaria):
                 - Bercak besar coklat/hitam, meluas cepat
                 - Area basah/layu di sekitar bercak
                 - Daun cepat mati
           
              * Bercak Daun Jamur (Leaf Spot - Cercospora/Septoria):
                 - Bercak bulat/oval dengan zona konsentris
                 - Pusat bercak abu-abu/coklat, tepi gelap
                 - Sering ada titik hitam kecil (piknidium)
           
              * Antraknosa (Anthracnose - Colletotrichum):
                 - Bercak cekung (sunken), nekrotik
                 - Tepi gelap kecoklatan
                 - Mungkin ada massa spora pink/orange saat lembab
           
              * Karat Daun (Rust - Puccinia):
                 - Pustula orange/kuning seperti karat
                 - Bubuk spora mudah lepas saat disentuh
                 - Biasanya di permukaan bawah daun
           
              * Embun Tepung (Powdery Mildew):
                 - Lapisan putih seperti tepung di permukaan daun
                 - Mudah dihapus tapi akan muncul lagi
        
          B. PENYAKIT INFEKSI BAKTERI (Bacterial Diseases):
              Ciri khas:
              - Bercak BASAH (water-soaked lesions)
              - Ada HALO kuning di sekitar bercak
              - Bercak angular (mengikuti tulang daun)
              - Mungkin ada ooze/lendir bakteri
              - Bau busuk (pada kasus parah)
           
              Jenis spesifik:
              * Bercak Bakteri (Bacterial Spot - Xanthomonas):
                 - Bercak kecil angular dengan halo kuning
                 - Permukaan kasar (scabby)
           
              * Hawar Bakteri (Bacterial Blight):
                 - Bercak besar basah, coklat kehitaman
                 - Menyebar cepat di kondisi lembab
           
              * Busuk Lunak (Soft Rot - Erwinia):
                 - Jaringan lunak, basah, busuk
                 - Bau busuk khas
                 - Area berair
        
          C. PENYAKIT VIRUS (Viral Diseases):
              Ciri khas:
              - Pola MOZAIK (kuning-hijau tidak teratur)
              - DISTORSI daun (keriting, menggulung)
              - Pertumbuhan STUNTED (kerdil)
              - Vein clearing (tulang daun terlihat transparan)
              - Tidak ada bercak dengan tepi jelas
           
              Jenis spesifik:
              * Virus Mozaik (Mosaic Virus - TMV/CMV):
                 - Pola kuning-hijau belang tidak teratur
                 - Daun keriting/terdistorsi
           
              * Virus Kuning (Yellowing Virus):
                 - Menguning tidak merata
                 - Daun kecil, pertumbuhan terhambat
        
          D. DEFISIENSI NUTRISI (Nutrient Deficiencies):
              Ciri khas:
              - Perubahan warna MERATA dan SIMETRIS
              - Pola teratur: dari tepi ke dalam ATAU dari ujung ke pangkal
              - TIDAK ADA BERCAK dengan tepi jelas
              - Perubahan warna gradual (smooth transition)
              - Mempengaruhi daun tua/muda secara KONSISTEN
           
              Jenis spesifik:
              * Defisiensi Nitrogen (N):
                 - Klorosis MERATA pada seluruh daun
                 - Daun TUA menguning lebih dulu
                 - Daun kecil, pertumbuhan lambat
           
              * Defisiensi Kalium (K):
                 - Klorosis dari TEPI DAUN ke dalam
                 - Nekrosis (coklat/kering) pada tepi
                 - Tepi menggulung ke bawah
                 - Daun TUA terpengaruh lebih dulu
           
              * Defisiensi Magnesium (Mg):
                 - Klorosis INTERVEINAL (antar tulang daun)
                 - Tulang daun tetap HIJAU
                 - Daun TUA terpengaruh lebih dulu
           
              * Defisiensi Besi (Fe):
                 - Klorosis INTERVEINAL
                 - Tulang daun tetap HIJAU
                 - Daun MUDA terpengaruh lebih dulu
           
              * Defisiensi Fosfor (P):
                 - Daun gelap keunguan/kebiruan
                 - Daun tua terpengaruh dulu
           
              * Defisiensi Kalsium (Ca):
                 - Nekrosis ujung daun muda
                 - Daun muda cacat/terdistorsi
        
          E. SERANGAN HAMA (Pest Damage):
              Ciri khas:
              - LUBANG bekas gigitan (bukan bercak)
              - JALUR makan (leaf miner tracks)
              - DEFORMASI dari hisapan (aphid, thrips)
              - Bekas luka fisik yang jelas
              - Mungkin ada serangga atau telur terlihat
           
              Jenis spesifik:
              * Ulat/Kupu-kupu:
                 - Lubang besar, tepi bekas gigitan
           
              * Leaf Miner:
                 - Jalur berkelok-kelok di dalam daun
           
              * Aphid/Thrips:
                 - Daun menggulung, keriting
                 - Warna pucat/keperakan
        
          F. STRESS LINGKUNGAN (Environmental Stress):
              Ciri khas:
              - Kerusakan SERAGAM di area terkena stress
              - Tidak ada pola penyebaran seperti infeksi
              - Gejala muncul mendadak setelah perubahan lingkungan
           
              Jenis spesifik:
              * Sunburn (Sengatan Matahari):
                 - Bercak putih/coklat di area terkena sinar langsung
                 - Tekstur kering
           
              * Cold Damage (Kerusakan Dingin):
                 - Daun layu, warna pucat merata
                 - Nekrosis pada ujung
           
              * Water Stress (Stress Air):
                 - Layu, mengering dari tepi
                 - Daun menguning seragam
        
          G. KOMBINASI (Bisa terjadi bersamaan):
              - Defisiensi nutrisi → tanaman lemah → mudah terserang penyakit
              - Stress lingkungan → pintu masuk patogen
              - Serangan hama → luka → infeksi sekunder
              - Lihat apakah ada gejala LEBIH DARI SATU kategori
        
          LANGKAH ANALISIS (SYSTEMATIC APPROACH):
        
          1. IDENTIFIKASI JENIS KERUSAKAN:
              - Apakah ada BERCAK dengan tepi jelas? → Kemungkinan JAMUR/BAKTERI
              - Apakah bercak BASAH dengan halo? → Kemungkinan BAKTERI
              - Apakah ada BUBUK/FUZZ? → Kemungkinan JAMUR
              - Apakah ada LUBANG gigitan? → Kemungkinan HAMA
              - Apakah perubahan warna MERATA? → Kemungkinan DEFISIENSI/STRESS
              - Apakah ada pola MOZAIK? → Kemungkinan VIRUS
        
          2. ANALISIS POLA DISTRIBUSI:
              - RANDOM/Tidak teratur → Infeksi (jamur/bakteri)
              - MERATA/Simetris → Defisiensi nutrisi atau stress lingkungan
              - Dari TEPI ke dalam → Defisiensi Kalium atau water stress
              - INTERVEINAL (antar tulang) → Defisiensi Mg/Fe
              - MENYELURUH → Defisiensi Nitrogen
        
          3. CEK BAGIAN DAUN TERPENGARUH:
              - Daun TUA lebih parah → N, P, K, Mg deficiency
              - Daun MUDA lebih parah → Fe, Ca deficiency atau virus
              - ACAK tanpa pola → Infeksi jamur/bakteri
        
          4. PERHATIKAN KARAKTERISTIK KHUSUS:
              - Zona konsentris (cincin) → Jamur tertentu (Cercospora, Alternaria)
              - Halo kuning → Bakteri (Xanthomonas)
              - Pustula orange → Karat (Puccinia)
              - Lapisan putih → Embun tepung
              - Jalur berkelok → Leaf miner
              - Daun menggulung → Aphid, virus, atau defisiensi Ca
        
          5. EVALUASI SEVERITY:
              - <10% area daun → Low severity
              - 10-40% area daun → Medium severity
              - >40% area daun → High severity
              - Multiple symptoms → Potentially combined issues
        
          6. DIFFERENTIAL DIAGNOSIS:
              - List 2-3 kemungkinan diagnosis alternatif
              - Jelaskan mengapa diagnosis utama lebih mungkin
              - Sebutkan indikator yang membedakan
        
          Berikan response dalam format JSON dengan struktur berikut:
          {
                "disease_id": "nama_kondisi_tanpa_spasi",
                "disease_name": "Nama Kondisi dalam Bahasa Indonesia",
                "scientific_name": "Nama ilmiah penyakit/patogen/defisiensi",
                "confidence": 0.85,
                "category": "INFECTIOUS_DISEASE atau NUTRIENT_DEFICIENCY atau HEALTHY atau ENVIRONMENTAL_STRESS",
                "severity": "Low/Medium/High/None",
                "symptoms": [
                     "Gejala visual 1 yang spesifik",
                     "Gejala visual 2 yang spesifik", 
                     "Gejala visual 3 yang spesifik"
                ],
                "differential_diagnosis": [
                     "Kondisi alternatif 1 yang mungkin",
                     "Kondisi alternatif 2 yang mungkin"
                ],
                "key_indicators": [
                     "Indikator kunci 1 yang menentukan diagnosis",
                     "Indikator kunci 2 yang menentukan diagnosis"
                ],
                "recommendations": [
                     "Rekomendasi perawatan spesifik 1",
                     "Rekomendasi perawatan spesifik 2",
                     "Rekomendasi perawatan spesifik 3",
                     "Rekomendasi perawatan spesifik 4"
                ],
                "prevention": [
                     "Cara pencegahan 1", 
                     "Cara pencegahan 2"
                ],
                "analysis_notes": "Analisis detail: mengapa diagnosis ini dipilih, indikator visual apa yang paling kuat, apakah ada keraguan"
          }
        
          KATEGORI KONDISI TANAMAN (COMPREHENSIVE):
        
          1. HEALTHY - Tanaman Sehat
              - Daun hijau merata, tidak ada bercak atau perubahan warna abnormal
              - Tekstur normal, tidak ada kerusakan fisik
        
          2. FUNGAL DISEASES (Penyakit Jamur):
              a) Hawar Daun (Blight):
                  - Phytophthora infestans, Alternaria solani
                  - Bercak besar coklat/hitam, meluas cepat, layu
           
              b) Bercak Daun Jamur (Leaf Spot):
                  - Cercospora, Septoria, Colletotrichum
                  - Bercak bulat dengan zona konsentris
           
              c) Antraknosa (Anthracnose):
                  - Colletotrichum spp.
                  - Bercak cekung, nekrotik, tepi gelap
           
              d) Karat Daun (Rust):
                  - Puccinia spp.
                  - Pustula orange/kuning, bubuk spora
           
              e) Embun Tepung (Powdery Mildew):
                  - Erysiphe, Sphaerotheca
                  - Lapisan putih seperti tepung
           
              f) Embun Bulu (Downy Mildew):
                  - Peronospora, Plasmopara
                  - Pertumbuhan fuzzy keabu-abuan di bawah daun
              g) Embun Jelaga (Sooty Mold):
                  - Capnodium, Fumago
                  - Lapisan HITAM TIPIS seperti jelaga/debu
                  - Tumbuh di permukaan (superficial)
                  - Bisa dihapus dengan tangan
                  - Biasanya ada honeydew dari serangga
                  - BUKAN bercak padat/solid dalam jaringan
   
                 PENTING: Bedakan dengan bercak hitam:
                  - Sooty mold = lapisan tipis di permukaan, seperti debu
                  - Black spot = bercak padat dalam jaringan daun
        
          3. BACTERIAL DISEASES (Penyakit Bakteri):
              a) Bercak Bakteri (Bacterial Spot):
                  - Xanthomonas campestris
                  - Bercak angular, halo kuning
           
              b) Hawar Bakteri (Bacterial Blight):
                  - Pseudomonas syringae, Xanthomonas
                  - Bercak basah, coklat kehitaman
           
              c) Busuk Lunak (Soft Rot):
                  - Erwinia, Pectobacterium
                  - Jaringan lunak, busuk, bau
           
              d) Kanker Bakteri (Bacterial Canker):
                  - Clavibacter michiganensis
                  - Luka terbuka, ooze bakteri
        
          4. VIRAL DISEASES (Penyakit Virus):
              a) Virus Mozaik (Mosaic Virus):
                  - TMV, CMV, PVY
                  - Pola mozaik kuning-hijau, distorsi
           
              b) Virus Kuning (Yellowing Virus):
                  - TYLCV (Tomato Yellow Leaf Curl)
                  - Menguning, menggulung, kerdil
           
              c) Virus Nekrosis:
                  - TSWV (Tomato Spotted Wilt)
                  - Bercak nekrotik, ring spots
        
          5. NUTRIENT DEFICIENCIES (Defisiensi Nutrisi):
              a) Defisiensi Nitrogen (N):
                  - Klorosis merata, daun tua menguning, pertumbuhan lambat
           
              b) Defisiensi Fosfor (P):
                  - Daun gelap keunguan, pertumbuhan terhambat
           
              c) Defisiensi Kalium (K):
                  - Nekrosis tepi daun, klorosis dari tepi, daun tua
           
              d) Defisiensi Magnesium (Mg):
                  - Klorosis interveinal, tulang hijau, daun tua
           
              e) Defisiensi Besi (Fe):
                  - Klorosis interveinal, tulang hijau, daun muda
           
              f) Defisiensi Kalsium (Ca):
                  - Nekrosis ujung, daun muda cacat, blossom end rot
           
              g) Defisiensi Sulfur (S):
                  - Klorosis daun muda, mirip N tapi daun muda dulu
           
              h) Defisiensi Zinc (Zn):
                  - Daun kecil, internode pendek, klorosis
           
              i) Defisiensi Boron (B):
                  - Daun tebal, rapuh, nekrosis ujung
        
          6. PEST DAMAGE (Serangan Hama):
              a) Kerusakan Ulat:
                  - Spodoptera, Helicoverpa
                  - Lubang besar, tepi bekas gigitan
           
              b) Leaf Miner:
                  - Liriomyza
                  - Jalur berkelok dalam daun
           
              c) Aphid Damage:
                  - Aphis, Myzus
                  - Daun menggulung, warna pucat, honeydew
           
              d) Thrips Damage:
                  - Thrips tabaci
                  - Bercak keperakan, distorsi
           
              e) Spider Mites:
                  - Tetranychus urticae
                  - Stippling (bintik putih), webbing
        
          7. ENVIRONMENTAL STRESS (Stress Lingkungan):
              a) Sunburn (Sun Scald):
                  - Bercak putih/coklat, tekstur kering, area terkena sinar
           
              b) Cold Damage (Chilling Injury):
                  - Daun layu pucat, nekrosis ujung
           
              c) Water Stress:
                  - Drought: Layu, mengering dari tepi
                  - Overwatering: Menguning merata, akar busuk
           
              d) Wind Damage:
                  - Robek fisik, tattered edges
           
              e) Chemical Burn (Herbicide/Pesticide):
                  - Distorsi, nekrosis, bleaching
        
          ATURAN PENTING:
          - Jika tanaman SEHAT: disease_id: "healthy", disease_name: "Tanaman Sehat"
          - Jika BUKAN FOTO DAUN: disease_id: "not_a_leaf", disease_name: "Bukan Foto Daun"
          - Confidence harus 0.0-1.0 (contoh: 0.85 untuk 85%)
          - Severity: None (sehat), Low (ringan), Medium (sedang), High (berat)
          - Berikan minimal 4 rekomendasi perawatan yang SPESIFIK dan PRAKTIS
          - Sebutkan di "analysis_notes" MENGAPA diagnosis ini dipilih (berdasarkan indikator visual apa)
          - Response HARUS valid JSON format
          - Fokus pada tanaman di Indonesia
          - JANGAN ASAL TEBAK - jika tidak yakin, confidence rendah dan sebutkan di differential_diagnosis
        
                CONTOH ANALYSIS_NOTES YANG BAIK:
                "Diagnosis defisiensi kalium dipilih karena: (1) klorosis dimulai dari tepi daun dengan pola merata, bukan bercak, (2) tepi daun menunjukkan nekrosis/pencoklatan, (3) tidak ada struktur patogen atau bercak dengan tepi jelas yang mengindikasikan infeksi jamur, (4) pola simetris pada kedua sisi daun. Confidence tinggi karena gejala sangat khas."
                """

        return prompt
        
    
    def predict(self, image_path: str) -> Optional[Dict]:
        """
        Predict plant disease menggunakan Gemini AI
        Pure AI vision analysis - No RAG dependency!
        
        Args:
            image_path: Path ke gambar tanaman
            
        Returns:
            Dictionary dengan hasil deteksi atau None jika error
        """
        try:
            # Verify file exists
            if not os.path.exists(image_path):
                logger.error(f"Image not found: {image_path}")
                return None
            
            # Load image
            logger.info(f"📸 Loading image: {image_path}")
            image = Image.open(image_path)
            
            # Resize jika terlalu besar (untuk efisiensi)
            max_size = 1024
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = (int(image.width * ratio), int(image.height * ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
                logger.info(f"Resized to: {new_size}")
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Create prompt
            prompt = self.create_detection_prompt()
            
            # Generate response from Gemini
            logger.info(f"Analyzing with Gemini AI...")
            response = self.model.generate_content([prompt, image])
            
            # Parse response
            if not response or not response.text:
                logger.error("Empty response from Gemini")
                return None
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            elif response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON: {e}")
                logger.error(f"Raw response: {response_text[:200]}")
                result = self._create_fallback_response(response_text)
            
            # Validate and enhance result
            result = self._validate_and_enhance_result(result)
            
            logger.info(f"Detection: {result['disease_name']} (Confidence: {result['confidence']:.1%})")
            
            return result
            
        except Exception as e:
            logger.error(f"Gemini prediction error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_fallback_response(self, response_text: str) -> Dict:
        """Create fallback response jika JSON parsing failed"""
        logger.warning("Creating fallback response from text")
        
        return {
            "disease_id": "unknown",
            "disease_name": "Analisis Tidak Lengkap",
            "scientific_name": "N/A",
            "confidence": 0.5,
            "severity": "Unknown",
            "symptoms": ["Analisis sedang diproses"],
            "recommendations": [
                "Coba upload foto yang lebih jelas",
                "Pastikan foto fokus pada daun/bagian yang sakit",
                "Gunakan pencahayaan yang baik",
                "Konsultasi dengan ahli pertanian lokal"
            ],
            "prevention": ["Monitor kondisi tanaman secara rutin"],
            "analysis_notes": response_text[:200]  # First 200 chars
        }
    
    def _validate_and_enhance_result(self, result: Dict) -> Dict:
        """Validate dan enhance result dari Gemini"""
        
        # Ensure required fields exist
        required_fields = {
            'disease_id': 'unknown',
            'disease_name': 'Tidak Teridentifikasi',
            'scientific_name': 'N/A',
            'confidence': 0.5,
            'severity': 'Unknown',
            'symptoms': [],
            'recommendations': [],
            'prevention': [],
            'analysis_notes': ''
        }
        
        for field, default in required_fields.items():
            if field not in result:
                result[field] = default
        
        # Validate confidence range
        try:
            confidence = float(result['confidence'])
            result['confidence'] = max(0.0, min(1.0, confidence))
        except (ValueError, TypeError):
            result['confidence'] = 0.5
        
        # Ensure lists are actually lists
        for field in ['symptoms', 'recommendations', 'prevention']:
            if not isinstance(result[field], list):
                result[field] = []
        
        # Add default recommendations if empty
        if not result['recommendations']:
            result['recommendations'] = [
                "Monitor kondisi tanaman secara rutin",
                "Pastikan drainase yang baik",
                "Jaga kebersihan area tanam",
                "Konsultasi dengan ahli jika diperlukan"
            ]
        
        # Add analysis method info
        result['analysis_method'] = 'Gemini AI Vision (Pure AI)'
        result['confidence_level'] = (
            'High' if result['confidence'] > 0.8 else
            'Medium' if result['confidence'] > 0.6 else
            'Low'
        )
        
        # Add formatted confidence percentage
        result['confidence_percentage'] = f"{result['confidence']*100:.1f}%"
        
        return result
    
    def analyze_batch(self, image_paths: List[str]) -> List[Dict]:
        """
        Analyze multiple images in batch
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            List of detection results
        """
        results = []
        
        logger.info(f"Batch analysis: {len(image_paths)} images")
        
        for i, image_path in enumerate(image_paths, 1):
            logger.info(f"[{i}/{len(image_paths)}] Processing: {image_path}")
            result = self.predict(image_path)
            if result:
                results.append(result)
            else:
                logger.warning(f"⚠️ Failed to process: {image_path}")
        
        logger.info(f"Batch complete: {len(results)}/{len(image_paths)} successful")
        
        return results


# Global model instance (singleton pattern)
_gemini_model: Optional[GeminiPlantDiseaseModel] = None

def load_gemini_model() -> GeminiPlantDiseaseModel:
    """Load or get Gemini model instance (singleton)"""
    global _gemini_model
    if _gemini_model is None:
        _gemini_model = GeminiPlantDiseaseModel()
        logger.info("Gemini AI Model loaded successfully")
        print("Gemini AI Plant Disease Detection Model ready!")
    return _gemini_model

def get_gemini_model() -> GeminiPlantDiseaseModel:
    """Get or create Gemini model instance (singleton)"""
    global _gemini_model
    if _gemini_model is None:
        _gemini_model = GeminiPlantDiseaseModel()
    return _gemini_model

def is_gemini_model_loaded() -> bool:
    """Check if Gemini model is loaded"""
    return _gemini_model is not None


# Test function
if __name__ == "__main__":
    print("="*50)
    print("TESTING GEMINI MODEL (NO RAG)")
    print("="*50)
    
    try:
        model = get_gemini_model()
        print("\n Model initialized successfully!")
        print("Ready for plant disease detection")
        print("100% FREE - No RAG dependency")
        
        # Test dengan sample image jika ada
        test_image = "test_leaf.jpg"
        if os.path.exists(test_image):
            print(f"\n Testing with: {test_image}")
            result = model.predict(test_image)
            
            if result:
                print("\n DETECTION RESULT:")
                print(f"   Disease: {result['disease_name']}")
                print(f"   Confidence: {result['confidence_percentage']}")
                print(f"   Severity: {result['severity']}")
                print(f"   Recommendations: {len(result['recommendations'])} items")
        else:
            print(f"\n⚠️ No test image found: {test_image}")
            
    except Exception as e:
        print(f"\n Error: {e}")
        import traceback
        traceback.print_exc()