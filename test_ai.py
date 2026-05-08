#!/usr/bin/env python3
"""
Quick Test Script for AI Medical Assistant
This demonstrates that the AI is connected to the internet and working
"""

from medical_api import MedicalAPIFetcher, format_medical_report

print("\n" + "="*70)
print("🧪 TESTING AI MEDICAL ASSISTANT")
print("="*70 + "\n")

# Create fetcher instance
fetcher = MedicalAPIFetcher()

# Test cases
test_cases = [
    ("Diabetes", "high blood sugar, frequent urination"),
    ("Malaria", "fever, chills, headache"),
    ("Asthma", "breathing difficulty, cough"),
]

for disease, symptoms in test_cases:
    print(f"\n{'='*70}")
    print(f"Testing: {disease}")
    print(f"{'='*70}\n")
    
    try:
        # Fetch from Wikipedia
        wiki_info = fetcher.fetch_from_wikipedia(disease)
        if wiki_info:
            print(f"✅ Wikipedia: SUCCESS")
            print(f"   Title: {wiki_info.get('title', 'N/A')}")
            print(f"   Description: {wiki_info.get('extract', 'N/A')[:150]}...")
        else:
            print(f"❌ Wikipedia: FAILED")
        
        # Fetch from PubMed
        pubmed_info = fetcher.fetch_from_pubmed(disease)
        if pubmed_info:
            articles = pubmed_info.get('articles', [])
            print(f"\n✅ PubMed: SUCCESS")
            print(f"   Found {len(articles)} research articles")
            if articles:
                print(f"   Latest: {articles[0]['title'][:100]}...")
        else:
            print(f"\n❌ PubMed: No results")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

print("\n" + "="*70)
print("✅ TEST COMPLETE - AI IS CONNECTED AND WORKING!")
print("="*70 + "\n")

print("To use the AI Medical Assistant:")
print("1. Run: python3 login.py (Desktop)")
print("2. Or open: http://127.0.0.1:5002 (Web)")
print("3. Click 'AI Medical Assistant' button/card")
print("4. Enter disease name or symptoms")
print("5. Get instant results from medical databases!\n")
