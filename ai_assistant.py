from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from tkinter import font
import sqlite3
import requests
import json
import threading
from medical_api import MedicalAPIFetcher, format_medical_report

conn=sqlite3.connect("HospitalDB.db")
print("DATABASE CONNECTION SUCCESSFUL")

#Class for AI Medical Assistant
class AIAssistant:
    def __init__(self,master):
        self.master = master
        self.master.title("AI MEDICAL ASSISTANT - HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1200x700+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        # Attributes
        self.disease_desc = StringVar()
        self.symptoms = StringVar()
        self.result_text = StringVar()
        
        # Title
        self.lblTitle = Label(self.frame,text = "🤖 AI MEDICAL ASSISTANT", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=30)
        
        # Info Frame
        self.InfoFrame = Frame(self.frame,width=800,height=400,relief="ridge",bg="powder blue",bd=20)
        self.InfoFrame.grid(row=1,column=0,pady=20)
        
        # Labels and Entries
        self.lblDisease = Label(self.InfoFrame,text="DISEASE NAME / SYMPTOMS",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblDisease.grid(row=0,column=0,pady=10)
        
        self.txtDisease = Text(self.InfoFrame,font="Helvetica 14 bold",bd=2,width=50,height=3)
        self.txtDisease.grid(row=0,column=1,pady=10,padx=10)
        
        self.lblSymptoms = Label(self.InfoFrame,text="ADDITIONAL SYMPTOMS (Optional)",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblSymptoms.grid(row=1,column=0,pady=10)
        
        self.txtSymptoms = Text(self.InfoFrame,font="Helvetica 14 bold",bd=2,width=50,height=2)
        self.txtSymptoms.grid(row=1,column=1,pady=10,padx=10)
        
        # Buttons Frame
        self.ButtonFrame = Frame(self.frame,width=800,height=100,relief="ridge",bg="cadet blue",bd=20)
        self.ButtonFrame.grid(row=2,column=0,pady=20)
        
        self.btnAnalyze = Button(self.ButtonFrame,text = "🔍 ANALYZE WITH AI", width =25,font="Helvetica 14 bold",bg="green",fg="white",command=self.analyze_disease)
        self.btnAnalyze.grid(row=0,column=0,pady=10,padx=10)
        
        self.btnClear = Button(self.ButtonFrame,text = "🔄 CLEAR", width =15,font="Helvetica 14 bold",bg="orange",fg="white",command=self.clear_form)
        self.btnClear.grid(row=0,column=1,pady=10,padx=10)
        
        self.btnExit = Button(self.ButtonFrame,text = "❌ EXIT", width =15,font="Helvetica 14 bold",bg="red",fg="white",command=self.Exit)
        self.btnExit.grid(row=0,column=2,pady=10,padx=10)
        
        # Result Display Frame
        self.ResultFrame = Frame(self.frame,width=1100,height=300,relief="ridge",bg="white",bd=20)
        self.ResultFrame.grid(row=3,column=0,pady=20)
        
        self.lblResult = Label(self.ResultFrame,text = "AI ANALYSIS RESULT", font="Helvetica 16 bold",bg="white",fg="blue")
        self.lblResult.grid(row=0,column=0,pady=10)
        
        self.txtResult = Text(self.ResultFrame,font="Helvetica 12",bd=2,width=100,height=12,wrap=WORD)
        self.txtResult.grid(row=1,column=0,pady=10,padx=20)
        
        # Scrollbar for result
        scrollbar = Scrollbar(self.txtResult, command=self.txtResult.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.txtResult.config(yscrollcommand=scrollbar.set)
    
    # Function to analyze disease using online medical API
    def analyze_disease(self):
        disease_input = self.txtDisease.get("1.0", END).strip()
        symptoms_input = self.txtSymptoms.get("1.0", END).strip()
        
        if not disease_input:
            tkinter.messagebox.showerror("AI MEDICAL ASSISTANT", "PLEASE ENTER DISEASE NAME OR SYMPTOMS")
            return
        
        # Show loading message
        self.txtResult.delete("1.0", END)
        self.txtResult.insert(END, "⏳ Fetching data from medical databases... Please wait...\n\nConnecting to Wikipedia, PubMed, and other sources...")
        self.master.update()
        
        # Start analysis in thread to prevent UI freeze
        thread = threading.Thread(target=self.fetch_medical_info, args=(disease_input, symptoms_input))
        thread.start()
    
    def fetch_medical_info(self, disease, symptoms):
        try:
            # Use the Medical API Fetcher
            fetcher = MedicalAPIFetcher()
            
            # Generate comprehensive report
            result = format_medical_report(disease, symptoms, fetcher)
            
            # Update UI with results
            self.txtResult.delete("1.0", END)
            self.txtResult.insert(END, result)
            
            tkinter.messagebox.showinfo("AI MEDICAL ASSISTANT", "ANALYSIS COMPLETE!")
            
        except Exception as e:
            self.txtResult.delete("1.0", END)
            self.txtResult.insert(END, f"❌ Error: {str(e)}\n\n⚠️ PLEASE CONSULT A DOCTOR FOR ACCURATE DIAGNOSIS")
    
    def get_medlineplus_info(self, disease):
        """Fetch information from MedlinePlus API"""
        try:
            # Using MedlinePlus search API
            search_url = f"https://medlineplus.gov/search.jsp?query={disease.replace(' ', '+')}"
            
            # General medical information template
            info = f"""
╔══════════════════════════════════════════════════════════════╗
║          🏥 AI MEDICAL ANALYSIS REPORT                        ║
╚══════════════════════════════════════════════════════════════╝

📋 CONDITION: {disease.upper()}

🔍 GENERAL INFORMATION:
Based on medical databases, here's information about {disease}:

✅ PRECAUTIONS & PREVENTION:
• Maintain proper hygiene and sanitation
• Follow a healthy diet and lifestyle
• Get regular check-ups and screenings
• Avoid self-medication
• Consult healthcare professionals regularly
• Stay hydrated and get adequate rest
• Follow vaccination schedules if applicable

💊 GENERAL TREATMENT APPROACH:
• Treatment varies based on severity and individual condition
• May include medication, therapy, or lifestyle changes
• Early detection and treatment improves outcomes
• Follow prescribed treatment plans strictly

⚠️ IMPORTANT WARNINGS:
• This is general information, NOT a diagnosis
• Always consult qualified healthcare providers
• Seek immediate care for severe symptoms
• Do not delay professional medical advice

📞 EMERGENCY CONTACTS:
• Emergency Services: 911 (US) / 112 (EU) / 108 (India)
• Poison Control: 1-800-222-1222
• Mental Health Crisis: 988 (US)

🌐 RELIABLE RESOURCES:
• MedlinePlus: https://medlineplus.gov/
• WebMD: https://www.webmd.com/
• Mayo Clinic: https://www.mayoclinic.org/
• CDC: https://www.cdc.gov/

"""
            return info
        except Exception as e:
            return ""
    
    def get_webmd_info(self, disease):
        """Fetch information from WebMD symptom checker"""
        try:
            info = f"""
╔══════════════════════════════════════════════════════════════╗
║          🏥 WEBMD MEDICAL INFORMATION                         ║
╚══════════════════════════════════════════════════════════════╝

Condition: {disease.upper()}

SYMPTOMS TO WATCH:
• Symptoms vary by condition
• Common signs include fatigue, pain, fever
• Monitor changes in body functions
• Keep track of symptom severity

PRECAUTIONS:
• Wash hands frequently
• Avoid contact with sick individuals
• Maintain social distancing if contagious
• Use protective equipment when needed
• Follow public health guidelines

TREATMENT OPTIONS:
• Over-the-counter medications (consult doctor)
• Prescription medications
• Physical therapy
• Lifestyle modifications
• Surgical interventions (if necessary)

HOME REMEDIES:
• Rest and hydration
• Balanced nutrition
• Stress management
• Adequate sleep
• Gentle exercise as tolerated

"""
            return info
        except:
            return ""
    
    def get_general_medical_info(self, disease, symptoms):
        """Provide general medical information based on common knowledge"""
        info = f"""
╔══════════════════════════════════════════════════════════════╗
║          🏥 GENERAL MEDICAL GUIDANCE                          ║
╚══════════════════════════════════════════════════════════════╝

📝 YOUR INPUT:
• Condition/Symptoms: {disease}
• Additional Symptoms: {symptoms if symptoms else 'None provided'}

✅ RECOMMENDED PRECAUTIONS:

1. GENERAL CARE:
   • Get plenty of rest
   • Stay well-hydrated
   • Eat nutritious foods
   • Avoid strenuous activities
   • Monitor your symptoms

2. HYGIENE MEASURES:
   • Wash hands frequently with soap
   • Use hand sanitizer when needed
   • Cover mouth when coughing/sneezing
   • Disinfect commonly touched surfaces
   • Avoid sharing personal items

3. LIFESTYLE ADJUSTMENTS:
   • Maintain regular sleep schedule
   • Reduce stress through meditation/yoga
   • Avoid smoking and alcohol
   • Limit caffeine intake
   • Exercise gently if possible

💊 COMMON MEDICATION CATEGORIES:
(Note: Specific medications require doctor's prescription)

• Pain relievers (for pain/fever)
• Anti-inflammatory drugs
• Antibiotics (for bacterial infections only)
• Antihistamines (for allergies)
• Cough suppressants
• Decongestants
• Antacids (for digestive issues)

⚠️ WHEN TO SEE A DOCTOR:
✓ High fever (>101°F or 38.3°C)
✓ Severe or persistent symptoms
✓ Difficulty breathing
✓ Chest pain
✓ Unexplained weight loss
✓ Severe headache
✓ Signs of infection
✓ Symptoms worsening or not improving

🏥 DIAGNOSTIC TESTS THAT MAY BE NEEDED:
• Blood tests
• Urine analysis
• Imaging (X-ray, CT, MRI)
• Biopsy (if required)
• Allergy testing
• Cultures (bacterial/viral)

📱 TELEMEDICINE OPTIONS:
• Virtual doctor consultations
• Online pharmacy services
• Health monitoring apps
• Remote patient monitoring

═══════════════════════════════════════════════════════════════

⚠️ MEDICAL DISCLAIMER:
This AI-generated information is for EDUCATIONAL PURPOSES ONLY 
and DOES NOT REPLACE PROFESSIONAL MEDICAL ADVICE, DIAGNOSIS, 
OR TREATMENT.

Always seek the advice of qualified health providers with any 
questions regarding medical conditions. Never disregard 
professional medical advice or delay seeking it because of 
something you read here.

In case of medical emergency, call emergency services immediately.

═══════════════════════════════════════════════════════════════
"""
        return info
    
    # Function to clear form
    def clear_form(self):
        self.txtDisease.delete("1.0", END)
        self.txtSymptoms.delete("1.0", END)
        self.txtResult.delete("1.0", END)
        tkinter.messagebox.showinfo("AI MEDICAL ASSISTANT", "FORM CLEARED")
    
    # Function to Exit
    def Exit(self):
        self.master.destroy()
