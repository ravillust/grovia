"""
Sync RAG Knowledge Files to Database

Script untuk sync file .txt di rag_knowledge/ ke database diseases
Run: python -m app.scripts.sync_rag_to_db
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.disease import Disease


class RAGParser:
    """Parser untuk file RAG knowledge .txt"""
    
    def __init__(self, rag_dir: str = "rag_knowledge"):
        self.rag_dir = Path(rag_dir)
        
    def parse_file(self, filepath: Path) -> Optional[Dict]:
        """Parse single RAG .txt file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip file if not valid disease knowledge
            if 'PENYEBAB:' not in content:
                print(f"[WARNING] Skipping {filepath.name} - not a disease knowledge file")
                return None
            
            # Extract disease name (first non-empty line after comments/quotes)
            lines = content.split('\n')
            disease_name = None
            for line in lines:
                clean_line = line.strip().strip('"\'')
                if clean_line and not clean_line.startswith('#') and not clean_line.startswith('"""'):
                    # Get main disease name (before any parenthesis)
                    if '(' in clean_line:
                        disease_name = clean_line.split('(')[0].strip()
                    else:
                        disease_name = clean_line.strip()
                    break
            
            if not disease_name:
                print(f"[WARNING] Cannot extract disease name from {filepath.name}")
                return None
            
            # Generate disease_id from filename
            disease_id = filepath.stem  # filename without extension
            
            # Extract sections
            sections = self._extract_sections(content)
            
            # Build disease data
            disease_data = {
                'disease_id': disease_id,
                'disease_name': disease_name,
                'scientific_name': self._extract_scientific_name(content),
                'description': self._extract_description(content),
                'symptoms': self._format_list(sections.get('GEJALA KHAS', [])),
                'causes': self._format_list(sections.get('PENYEBAB', [])),
                'affected_plants': self._format_list(sections.get('TANAMAN RENTAN', [])),
                'prevention': self._format_list(sections.get('PENCEGAHAN', [])),
                'treatment': self._format_list(sections.get('PENGOBATAN', [])),
                'organic_solutions': self._extract_organic_solutions(sections),
                'chemical_solutions': self._extract_chemical_solutions(sections),
                'additional_tips': self._format_additional_tips(sections),
                'thumbnail': None,  # Will be set manually or via migration
                'images': json.dumps([])
            }
            
            return disease_data
            
        except Exception as e:
            print(f"[ERROR] Error parsing {filepath.name}: {str(e)}")
            return None
    
    def _extract_sections(self, content: str) -> Dict[str, List[str]]:
        """Extract all sections from content"""
        sections = {}
        current_section = None
        current_items = []
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Check if line is a section header
            if line and line.isupper() and ':' in line:
                # Save previous section
                if current_section:
                    sections[current_section] = current_items
                
                # Start new section
                current_section = line.replace(':', '').strip()
                current_items = []
            
            # Add item to current section
            elif line and current_section:
                # Remove leading dash/bullet
                item = line.lstrip('-•*').strip()
                if item:
                    current_items.append(item)
        
        # Save last section
        if current_section:
            sections[current_section] = current_items
        
        return sections
    
    def _extract_scientific_name(self, content: str) -> str:
        """Extract scientific name (text in parentheses or italic)"""
        # Try to find text in parentheses after disease name
        match = re.search(r'\(([A-Z][a-z]+\s+[a-z]+.*?)\)', content)
        if match:
            return match.group(1)
        
        # Try to find italic format or known patterns
        match = re.search(r'[A-Z][a-z]+\s+[a-z]+(?:\s+[a-z]+)?', content)
        if match:
            return match.group(0)
        
        return "Unknown"
    
    def _extract_description(self, content: str) -> str:
        """Extract description from comments or first paragraph"""
        lines = content.split('\n')
        descriptions = []
        
        in_comment = False
        for line in lines:
            clean_line = line.strip().strip('"\'')
            
            # Check for comment blocks
            if '"""' in clean_line:
                in_comment = not in_comment
                continue
            
            if in_comment and clean_line and not clean_line.startswith('#'):
                descriptions.append(clean_line)
        
        if descriptions:
            return ' '.join(descriptions[:3])  # First 3 lines
        
        # Fallback: use disease name
        return f"Penyakit tanaman yang disebabkan oleh patogen"
    
    def _format_list(self, items: List[str]) -> str:
        """Format list items as JSON array"""
        return json.dumps(items, ensure_ascii=False)
    
    def _extract_organic_solutions(self, sections: Dict) -> Optional[str]:
        """Extract organic solutions from treatment section"""
        treatment = sections.get('PENGOBATAN', [])
        organic = []
        
        for item in treatment:
            # Look for organic keywords
            if any(keyword in item.lower() for keyword in ['bio', 'organik', 'alami', 'kompos', 'trichoderma', 'bacillus']):
                organic.append(item)
        
        return json.dumps(organic, ensure_ascii=False) if organic else None
    
    def _extract_chemical_solutions(self, sections: Dict) -> Optional[str]:
        """Extract chemical solutions from treatment section"""
        treatment = sections.get('PENGOBATAN', [])
        chemical = []
        
        for item in treatment:
            # Look for chemical keywords
            if any(keyword in item.lower() for keyword in ['fungisida', 'pestisida', 'bakterisida', 'kimia', 'chemical']):
                chemical.append(item)
        
        return json.dumps(chemical, ensure_ascii=False) if chemical else None
    
    def _format_additional_tips(self, sections: Dict) -> Optional[str]:
        """Format additional tips from various sections"""
        tips = []
        
        # Add differential diagnosis
        if 'DIAGNOSIS PEMBEDA' in sections:
            tips.extend(sections['DIAGNOSIS PEMBEDA'])
        
        # Add stage information
        if 'STAGE PERKEMBANGAN' in sections or 'STAGE' in sections:
            stage_key = 'STAGE PERKEMBANGAN' if 'STAGE PERKEMBANGAN' in sections else 'STAGE'
            tips.extend(sections[stage_key])
        
        # Add environmental triggers
        if 'KONDISI LINGKUNGAN PEMICU' in sections:
            tips.extend(sections['KONDISI LINGKUNGAN PEMICU'])
        
        return json.dumps(tips, ensure_ascii=False) if tips else None
    
    def parse_all(self) -> List[Dict]:
        """Parse all .txt files in rag_knowledge directory"""
        if not self.rag_dir.exists():
            print(f"[ERROR] Directory {self.rag_dir} not found!")
            return []
        
        diseases = []
        txt_files = list(self.rag_dir.glob('*.txt'))
        
        print(f"\n[INFO] Found {len(txt_files)} .txt files in {self.rag_dir}")
        print("=" * 60)
        
        for filepath in txt_files:
            print(f"\n[INFO] Parsing {filepath.name}...")
            disease_data = self.parse_file(filepath)
            
            if disease_data:
                diseases.append(disease_data)
                print(f"[SUCCESS] Successfully parsed: {disease_data['disease_name']}")
        
        print("\n" + "=" * 60)
        print(f"[SUCCESS] Total parsed: {len(diseases)} diseases")
        
        return diseases


class DatabaseSync:
    """Sync parsed data to database"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def sync_disease(self, disease_data: Dict) -> bool:
        """Sync single disease to database (insert or update)"""
        try:
            # Check if disease already exists
            existing = self.db.query(Disease).filter(
                Disease.disease_id == disease_data['disease_id']
            ).first()
            
            if existing:
                # Update existing
                for key, value in disease_data.items():
                    if key != 'id':  # Don't update primary key
                        setattr(existing, key, value)
                
                print(f"[UPDATE] Updated: {disease_data['disease_name']}")
            else:
                # Insert new
                new_disease = Disease(**disease_data)
                self.db.add(new_disease)
                print(f"[INSERT] Inserted: {disease_data['disease_name']}")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Error syncing {disease_data['disease_name']}: {str(e)}")
            return False
    
    def sync_all(self, diseases: List[Dict]) -> tuple:
        """Sync all diseases to database"""
        success_count = 0
        fail_count = 0
        
        print("\n" + "=" * 60)
        print("[INFO] Syncing to database...")
        print("=" * 60)
        
        for disease_data in diseases:
            if self.sync_disease(disease_data):
                success_count += 1
            else:
                fail_count += 1
        
        try:
            self.db.commit()
            print("\n" + "=" * 60)
            print(f"[SUCCESS] Sync completed!")
            print(f"   - Success: {success_count}")
            print(f"   - Failed: {fail_count}")
            print("=" * 60)
        except Exception as e:
            self.db.rollback()
            print(f"\n[ERROR] Database commit failed: {str(e)}")
            return (0, len(diseases))
        
        return (success_count, fail_count)


def main():
    """Main sync process"""
    print("\n" + "=" * 60)
    print("RAG Knowledge to Database Sync")
    print("=" * 60)
    
    # Parse RAG files
    parser = RAGParser()
    diseases = parser.parse_all()
    
    if not diseases:
        print("\n[WARNING] No diseases to sync!")
        return
    
    # Create database tables if not exist
    Base.metadata.create_all(bind=engine)
    
    # Sync to database
    db = SessionLocal()
    try:
        syncer = DatabaseSync(db)
        success, failed = syncer.sync_all(diseases)
        
        if failed == 0:
            print("\n[SUCCESS] All diseases synced successfully!")
        else:
            print(f"\n[WARNING] {failed} diseases failed to sync")
    
    finally:
        db.close()
    
    print("\n[INFO] Done!\n")


if __name__ == "__main__":
    main()
