"""
AI Medical Information Fetcher
Connects to various medical APIs and databases worldwide
"""

import requests
import json
from typing import Dict, List, Optional

class MedicalAPIFetcher:
    """Fetch medical information from various online sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'en-US,en;q=0.9'
        })
    
    def fetch_from_medlineplus(self, disease: str) -> Optional[Dict]:
        """
        Fetch information from MedlinePlus (NIH)
        Free medical encyclopedia API
        """
        try:
            # MedlinePlus search API
            url = "https://medlineplus.gov/download/api/search.json"
            params = {
                'query': disease,
                'limit': 5
            }
            
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'source': 'MedlinePlus (NIH)',
                    'data': data,
                    'url': f"https://medlineplus.gov/search.jsp?query={disease.replace(' ', '+')}"
                }
        except Exception as e:
            print(f"MedlinePlus error: {e}")
        
        return None
    
    def fetch_from_wikipedia(self, disease: str) -> Optional[Dict]:
        """
        Fetch medical information from Wikipedia
        """
        try:
            url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
            params = {
                'title': disease,
                'redirect': True
            }
            
            response = self.session.get(url + disease, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data:
                    return {
                        'source': 'Wikipedia Medical',
                        'title': data.get('title', ''),
                        'description': data.get('extract', ''),
                        'url': data.get('content_urls', {}).get('desktop', {}).get('page', '')
                    }
        except Exception as e:
            print(f"Wikipedia error: {e}")
        
        return None
    
    def fetch_from_pubmed(self, disease: str) -> Optional[Dict]:
        """
        Fetch research articles from PubMed (NCBI)
        """
        try:
            # PubMed E-utilities API
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            params = {
                'db': 'pubmed',
                'term': disease,
                'retmax': 5,
                'retmode': 'json'
            }
            
            response = self.session.get(base_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                ids = data.get('esearchresult', {}).get('idlist', [])
                
                if ids:
                    # Fetch summaries for these articles
                    summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                    summary_params = {
                        'db': 'pubmed',
                        'id': ','.join(ids[:3]),
                        'retmode': 'json'
                    }
                    
                    summary_response = self.session.get(summary_url, params=summary_params, timeout=10)
                    if summary_response.status_code == 200:
                        summary_data = summary_response.json()
                        articles = []
                        for pmid in ids[:3]:
                            if pmid in summary_data.get('result', {}):
                                article = summary_data['result'][pmid]
                                articles.append({
                                    'title': article.get('title', ''),
                                    'authors': article.get('authors', []),
                                    'journal': article.get('fulljournalname', ''),
                                    'pubdate': article.get('pubdate', ''),
                                    'doi': article.get('doi', '')
                                })
                        
                        return {
                            'source': 'PubMed (NCBI)',
                            'articles': articles,
                            'url': f"https://pubmed.ncbi.nlm.nih.gov/?term={disease.replace(' ', '+')}"
                        }
        except Exception as e:
            print(f"PubMed error: {e}")
        
        return None
    
    def fetch_drug_info(self, drug_name: str) -> Optional[Dict]:
        """
        Fetch drug information from DailyMed (FDA)
        """
        try:
            url = f"https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json"
            params = {
                'search': drug_name,
                'limit': 5
            }
            
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'source': 'DailyMed (FDA)',
                    'data': data,
                    'url': f"https://dailymed.nlm.nih.gov/dailymed/search.cfm?query={drug_name.replace(' ', '+')}"
                }
        except Exception as e:
            print(f"DailyMed error: {e}")
        
        return None
    
    def get_general_precautions(self, disease_category: str) -> List[str]:
        """
        Return general precautions based on disease category
        """
        precautions_db = {
            'infection': [
                'Wash hands frequently with soap and water',
                'Use alcohol-based hand sanitizer',
                'Avoid close contact with sick individuals',
                'Cover mouth and nose when coughing or sneezing',
                'Disinfect frequently touched surfaces',
                'Stay home when sick',
                'Get recommended vaccinations'
            ],
            'cardiovascular': [
                'Maintain a heart-healthy diet low in sodium',
                'Exercise regularly (30 minutes most days)',
                'Monitor blood pressure regularly',
                'Avoid smoking and limit alcohol',
                'Manage stress through relaxation techniques',
                'Maintain healthy weight',
                'Take prescribed medications as directed'
            ],
            'diabetes': [
                'Monitor blood sugar levels regularly',
                'Follow a balanced diabetic diet',
                'Exercise regularly',
                'Take insulin/medications as prescribed',
                'Maintain healthy weight',
                'Check feet daily for injuries',
                'Get regular eye and dental checkups'
            ],
            'respiratory': [
                'Avoid smoking and secondhand smoke',
                'Use air purifiers if needed',
                'Practice breathing exercises',
                'Avoid respiratory irritants',
                'Get flu and pneumonia vaccines',
                'Maintain good posture',
                'Stay hydrated'
            ],
            'general': [
                'Maintain a balanced diet rich in fruits and vegetables',
                'Exercise regularly (at least 150 minutes per week)',
                'Get 7-9 hours of quality sleep',
                'Manage stress through meditation or yoga',
                'Stay hydrated (8 glasses of water daily)',
                'Avoid tobacco and limit alcohol',
                'Get regular health checkups',
                'Maintain healthy body weight',
                'Practice good hygiene',
                'Wear sunscreen when outdoors'
            ]
        }
        
        disease_category = disease_category.lower()
        
        # Match category
        if 'infect' in disease_category or 'virus' in disease_category or 'bacteria' in disease_category:
            return precautions_db['infection']
        elif 'heart' in disease_category or 'cardio' in disease_category or 'blood pressure' in disease_category:
            return precautions_db['cardiovascular']
        elif 'diabet' in disease_category or 'sugar' in disease_category:
            return precautions_db['diabetes']
        elif 'asthma' in disease_category or 'lung' in disease_category or 'breath' in disease_category:
            return precautions_db['respiratory']
        else:
            return precautions_db['general']
    
    def get_common_medicines(self, symptoms: str) -> List[Dict]:
        """
        Return common medicine categories (NOT prescriptions - just information)
        """
        medicine_db = {
            'pain': [
                {'category': 'Analgesics', 'examples': 'Acetaminophen, Ibuprofen', 'use': 'Pain relief'},
                {'category': 'NSAIDs', 'examples': 'Aspirin, Naproxen', 'use': 'Pain and inflammation'}
            ],
            'fever': [
                {'category': 'Antipyretics', 'examples': 'Acetaminophen, Ibuprofen', 'use': 'Reduce fever'}
            ],
            'allergy': [
                {'category': 'Antihistamines', 'examples': 'Cetirizine, Loratadine', 'use': 'Allergy relief'},
                {'category': 'Decongestants', 'examples': 'Pseudoephedrine', 'use': 'Nasal congestion'}
            ],
            'infection': [
                {'category': 'Antibiotics', 'examples': 'Amoxicillin, Azithromycin', 'use': 'Bacterial infections (prescription only)'},
                {'category': 'Antivirals', 'examples': 'Oseltamivir', 'use': 'Viral infections (prescription only)'}
            ],
            'digestive': [
                {'category': 'Antacids', 'examples': 'Calcium carbonate', 'use': 'Acid reflux'},
                {'category': 'Proton Pump Inhibitors', 'examples': 'Omeprazole', 'use': 'GERD'}
            ],
            'general': [
                {'category': 'Multivitamins', 'examples': 'Various brands', 'use': 'Nutritional support'},
                {'category': 'Electrolytes', 'examples': 'ORS solutions', 'use': 'Hydration'}
            ]
        }
        
        symptoms = symptoms.lower()
        
        if 'pain' in symptoms or 'ache' in symptoms:
            return medicine_db['pain']
        elif 'fever' in symptoms or 'temperature' in symptoms:
            return medicine_db['fever']
        elif 'allerg' in symptoms or 'sneeze' in symptoms or 'itch' in symptoms:
            return medicine_db['allergy']
        elif 'infect' in symptoms or 'bacteria' in symptoms:
            return medicine_db['infection']
        elif 'stomach' in symptoms or 'digest' in symptoms or 'acid' in symptoms:
            return medicine_db['digestive']
        else:
            return medicine_db['general']


def format_medical_report(disease: str, symptoms: str, fetcher: MedicalAPIFetcher) -> str:
    """
    Generate comprehensive medical information report
    """
    report = []
    report.append("╔══════════════════════════════════════════════════════════════╗")
    report.append("║          🏥 AI MEDICAL INFORMATION REPORT                      ║")
    report.append("╚══════════════════════════════════════════════════════════════╝")
    report.append("")
    report.append(f"📋 CONDITION: {disease.upper()}")
    if symptoms:
        report.append(f"➕ SYMPTOMS: {symptoms.upper()}")
    report.append("")
    
    # Fetch from Wikipedia
    wiki_info = fetcher.fetch_from_wikipedia(disease)
    if wiki_info:
        report.append("━" * 60)
        report.append("📖 GENERAL INFORMATION (Wikipedia):")
        report.append("━" * 60)
        report.append(wiki_info['description'][:500] + "...")
        report.append(f"\n🔗 Read more: {wiki_info['url']}")
        report.append("")
    
    # Fetch from MedlinePlus
    medline_info = fetcher.fetch_from_medlineplus(disease)
    if medline_info:
        report.append("━" * 60)
        report.append("🏛️ MEDICAL RESOURCES (MedlinePlus - NIH):")
        report.append("━" * 60)
        report.append(f"🔗 Search results: {medline_info['url']}")
        report.append("")
    
    # Fetch from PubMed
    pubmed_info = fetcher.fetch_from_pubmed(disease)
    if pubmed_info:
        report.append("━" * 60)
        report.append("📚 RESEARCH ARTICLES (PubMed):")
        report.append("━" * 60)
        for i, article in enumerate(pubmed_info.get('articles', [])[:3], 1):
            report.append(f"{i}. {article['title']}")
            report.append(f"   Journal: {article['journal']}")
            report.append(f"   Published: {article['pubdate']}")
            report.append("")
        report.append(f"🔗 View all: {pubmed_info['url']}")
        report.append("")
    
    # Add precautions
    report.append("━" * 60)
    report.append("✅ RECOMMENDED PRECAUTIONS:")
    report.append("━" * 60)
    precautions = fetcher.get_general_precautions(disease)
    for i, precaution in enumerate(precautions, 1):
        report.append(f"  {i}. {precaution}")
    report.append("")
    
    # Add medicine information
    report.append("━" * 60)
    report.append("💊 COMMON MEDICINE CATEGORIES (Information Only):")
    report.append("━" * 60)
    medicines = fetcher.get_common_medicines(symptoms if symptoms else disease)
    for med in medicines:
        report.append(f"• {med['category']}")
        report.append(f"  Examples: {med['examples']}")
        report.append(f"  Use: {med['use']}")
    report.append("")
    report.append("⚠️ NOTE: Always consult a doctor before taking any medication!")
    report.append("")
    
    # Emergency contacts
    report.append("━" * 60)
    report.append("📞 EMERGENCY CONTACTS:")
    report.append("━" * 60)
    report.append("• Emergency Services: 911 (US) / 112 (EU) / 108 (India)")
    report.append("• Poison Control: 1-800-222-1222")
    report.append("• Mental Health Crisis: 988 (US)")
    report.append("")
    
    # Disclaimer
    report.append("═" * 60)
    report.append("⚠️ MEDICAL DISCLAIMER:")
    report.append("This information is for EDUCATIONAL PURPOSES ONLY and does NOT")
    report.append("replace professional medical advice, diagnosis, or treatment.")
    report.append("Always consult qualified healthcare providers.")
    report.append("═" * 60)
    
    return "\n".join(report)


# Test function
if __name__ == "__main__":
    fetcher = MedicalAPIFetcher()
    
    print("Testing AI Medical Information Fetcher...")
    print("\nExample: Searching for 'Diabetes'\n")
    
    report = format_medical_report("Diabetes", "high blood sugar, frequent urination", fetcher)
    print(report)
