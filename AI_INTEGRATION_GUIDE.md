# AI Medical Assistant Integration Guide

## 🎯 Overview

The Hospital Management System now includes an **AI Medical Assistant** that connects to worldwide medical databases and provides:
- Disease information and descriptions
- Recommended precautions
- Common medicine categories (informational)
- Links to authoritative medical resources

## ✨ Features

### 1. **Multiple Data Sources**
- **Wikipedia Medical Articles** - General disease information
- **PubMed (NCBI)** - Latest research articles
- **MedlinePlus (NIH)** - Trusted medical encyclopedia
- **DailyMed (FDA)** - Drug information database

### 2. **Smart Information Retrieval**
- Automatic categorization of diseases
- Context-aware precautions
- Symptom-based medicine suggestions
- Emergency contact information

### 3. **User-Friendly Interface**
- Available on both Desktop (Tkinter) and Web (Flask)
- Real-time analysis with loading indicators
- Formatted reports with emojis for easy reading
- Medical disclaimer included

## 🚀 How to Use

### Desktop Application (Tkinter)

1. **Launch the application:**
   ```bash
   python3 login.py
   ```
   Or use the launcher:
   ```bash
   ./launch_app.command
   ```

2. **Login with credentials:**
   - Username: `admin` | Password: `1234`
   - OR Username: `root` | Password: `4321`

3. **Click on "🤖 AI MEDICAL ASSISTANT"** button in the main menu

4. **Enter disease/symptoms:**
   - Type the disease name or describe symptoms
   - Add additional symptoms (optional)
   - Click "ANALYZE WITH AI"

5. **View the results:**
   - Disease description from Wikipedia
   - Research articles from PubMed
   - Recommended precautions
   - Common medicine categories
   - Emergency contacts

### Web Application (Flask)

1. **Start the web server:**
   ```bash
   python3 app.py
   ```

2. **Open browser:** http://127.0.0.1:5002

3. **Login and click "🤖 AI Medical Assistant"** card

4. **Use the same interface as desktop**

## 📊 Example Usage

### Input:
```
Disease: Diabetes
Additional Symptoms: High blood sugar, frequent urination, excessive thirst
```

### Output Includes:
✅ **General Information** - What is diabetes
✅ **Precautions** - Diet, exercise, monitoring
✅ **Medicine Categories** - Insulin, oral medications (info only)
✅ **Research Articles** - Latest studies from PubMed
✅ **Resources** - Links to MedlinePlus, CDC, etc.
✅ **Emergency Contacts** - When to seek help

## 🔧 Technical Details

### Files Created/Modified:

1. **ai_assistant.py** - Desktop GUI for AI assistant
2. **medical_api.py** - API integration module
3. **app.py** - Added web route `/ai-assistant`
4. **menu.py** - Added AI Assistant button

### Dependencies:

```bash
pip3 install requests flask
```

### API Endpoints Used:

- Wikipedia API: `https://en.wikipedia.org/api/rest_v1/`
- PubMed E-utilities: `https://eutils.ncbi.nlm.nih.gov/`
- MedlinePlus: `https://medlineplus.gov/`
- DailyMed: `https://dailymed.nlm.nih.gov/`

## ⚠️ Important Disclaimers

1. **Educational Purpose Only** - Not a replacement for professional medical advice
2. **No Diagnosis** - Provides general information only
3. **Consult Doctors** - Always seek qualified healthcare providers
4. **Emergency** - Call 911/112/108 for medical emergencies
5. **Medication Info** - Shows categories, NOT prescriptions

## 🌐 Internet Connection Required

The AI Assistant needs internet access to fetch real-time data from:
- Medical databases
- Research journals
- Health organization websites

## 🎨 Customization

### Change Colors:
Edit the button colors in:
- `menu.py` line ~48 (desktop)
- `app.py` line ~423 (web)

### Add More APIs:
Extend `medical_api.py` by adding new fetcher methods:
```python
def fetch_from_new_api(self, query):
    # Your implementation
    pass
```

### Modify Report Format:
Edit `format_medical_report()` function in `medical_api.py`

## 📱 Future Enhancements

Potential additions:
- [ ] Machine Learning diagnosis support
- [ ] Image recognition for skin conditions
- [ ] Drug interaction checker
- [ ] Symptom checker with decision trees
- [ ] Multi-language support
- [ ] Telemedicine integration
- [ ] Appointment scheduling with specialists

## 🆘 Troubleshooting

### "No internet connection" errors:
- Check your network connection
- Verify firewall settings
- Some APIs may be temporarily unavailable

### "Module not found" errors:
```bash
pip3 install requests flask
```

### App doesn't start:
```bash
cd /Users/singampalliswamy/Desktop/Hospital-Management-System
python3 login.py
```

## 📞 Support

For technical issues with the AI integration, check:
- Console output for error messages
- Internet connectivity
- API rate limits (some services have limits)

---

**Created:** March 25, 2026
**Version:** 1.0
**Integration:** AI Medical Assistant with World Medical Databases
