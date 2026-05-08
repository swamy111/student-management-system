from tkinter import *
import tkinter.messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime

conn=sqlite3.connect("HospitalDB.db")
print("DATABASE CONNECTION SUCCESSFUL")

#Class for Nurse Dashboard
class NurseDashboard:
    def __init__(self,master):
        self.master = master
        self.master.title("NURSE DASHBOARD - HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1400x800+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        # Title
        self.lblTitle = Label(self.frame,text = "💉 NURSE STATION", font="Helvetica 24 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=4,pady=20)
        
        # Welcome Panel
        self.WelcomeFrame = Frame(self.frame,width=1300,height=100,relief="ridge",bg="powder blue",bd=20)
        self.WelcomeFrame.grid(row=1,column=0,pady=10)
        
        self.lblWelcome = Label(self.WelcomeFrame,text="Welcome, Nurse Sarah Johnson",font="Helvetica 18 bold",bg="powder blue",fg="#2c3e50")
        self.lblWelcome.grid(row=0,column=0,pady=10)
        
        self.lblShift = Label(self.WelcomeFrame,text="Shift: Morning (6AM-2PM) | Department: Emergency",font="Helvetica 14",bg="powder blue",fg="#555")
        self.lblShift.grid(row=1,column=0)
        
        # Main Menu Buttons
        self.MenuFrame = Frame(self.frame,width=1300,height=500,relief="ridge",bg="white",bd=20)
        self.MenuFrame.grid(row=2,column=0,pady=10)
        
        # Button 1: View Patients
        self.btnPatients = Button(self.MenuFrame,text = "👥 VIEW PATIENTS", width =25,font="Helvetica 16 bold",bg="#3498db",fg="white",command=self.VIEW_PATIENTS)
        self.btnPatients.grid(row=0,column=0,pady=20,padx=20)
        
        # Button 2: Medicine Management
        self.btnMedicine = Button(self.MenuFrame,text = "💊 MEDICINE MANAGEMENT", width =25,font="Helvetica 16 bold",bg="#e74c3c",fg="white",command=self.MEDICINE_MANAGEMENT)
        self.btnMedicine.grid(row=0,column=1,pady=20,padx=20)
        
        # Button 3: Doctor Schedule
        self.btnSchedule = Button(self.MenuFrame,text = "📅 DOCTOR SCHEDULE", width =25,font="Helvetica 16 bold",bg="#f39c12",fg="white",command=self.DOCTOR_SCHEDULE)
        self.btnSchedule.grid(row=1,column=0,pady=20,padx=20)
        
        # Button 4: Medical Assistant AI
        self.btnAI = Button(self.MenuFrame,text = "🤖 AI MEDICAL ASSISTANT", width =25,font="Helvetica 16 bold",bg="#2ecc71",fg="white",command=self.AI_ASSISTANT)
        self.btnAI.grid(row=1,column=1,pady=20,padx=20)
        
        # Button 5: Patient Vitals
        self.btnVitals = Button(self.MenuFrame,text = "❤️ PATIENT VITALS", width =25,font="Helvetica 16 bold",bg="#9b59b6",fg="white",command=self.PATIENT_VITALS)
        self.btnVitals.grid(row=2,column=0,pady=20,padx=20)
        
        # Button 6: Ward Management
        self.btnWard = Button(self.MenuFrame,text = "🏥 WARD MANAGEMENT", width =25,font="Helvetica 16 bold",bg="#1abc9c",fg="white",command=self.WARD_MANAGEMENT)
        self.btnWard.grid(row=2,column=1,pady=20,padx=20)
        
        # Button 7: Nursing Notes
        self.btnNotes = Button(self.MenuFrame,text = "📝 NURSING NOTES", width =25,font="Helvetica 16 bold",bg="#e67e22",fg="white",command=self.NURSING_NOTES)
        self.btnNotes.grid(row=3,column=0,pady=20,padx=20)
        
        # Button 8: Emergency Protocol
        self.btnEmergency = Button(self.MenuFrame,text = "🚨 EMERGENCY PROTOCOL", width =25,font="Helvetica 16 bold",bg="#c0392b",fg="white",command=self.EMERGENCY_PROTOCOL)
        self.btnEmergency.grid(row=3,column=1,pady=20,padx=20)
        
        # Exit Button
        self.btnExit = Button(self.MenuFrame,text = "❌ LOGOUT", width =25,font="Helvetica 16 bold",bg="#7f8c8d",fg="white",command=self.Exit)
        self.btnExit.grid(row=4,column=0,columnspan=2,pady=20)
    
    def VIEW_PATIENTS(self):
        self.newWindow = Toplevel(self.master)
        self.app = NurseViewPatients(self.newWindow)
    
    def MEDICINE_MANAGEMENT(self):
        self.newWindow = Toplevel(self.master)
        self.app = NurseMedicineMgmt(self.newWindow)
    
    def DOCTOR_SCHEDULE(self):
        self.newWindow = Toplevel(self.master)
        self.app = DoctorSchedule(self.newWindow)
    
    def AI_ASSISTANT(self):
        from ai_assistant import AIAssistant
        self.newWindow = Toplevel(self.master)
        self.app = AIAssistant(self.newWindow)
    
    def PATIENT_VITALS(self):
        self.newWindow = Toplevel(self.master)
        self.app = PatientVitals(self.newWindow)
    
    def WARD_MANAGEMENT(self):
        self.newWindow = Toplevel(self.master)
        self.app = WardManagement(self.newWindow)
    
    def NURSING_NOTES(self):
        self.newWindow = Toplevel(self.master)
        self.app = NursingNotes(self.newWindow)
    
    def EMERGENCY_PROTOCOL(self):
        self.newWindow = Toplevel(self.master)
        self.app = EmergencyProtocol(self.newWindow)
    
    def Exit(self):
        self.master.destroy()

# View Patients Class
class NurseViewPatients:
    def __init__(self,master):
        self.master = master
        self.master.title("VIEW PATIENTS - NURSE DASHBOARD")
        self.master.geometry("1400x700+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        self.lblTitle = Label(self.frame,text = "👥 PATIENT LIST", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=20)
        
        # Treeview
        self.TreeFrame = Frame(self.frame,width=1300,height=500,relief="ridge",bg="white",bd=20)
        self.TreeFrame.grid(row=1,column=0,pady=10)
        
        self.tree = ttk.Treeview(self.TreeFrame, columns=("ID", "Name", "Sex", "BG", "DOB", "Address", "Email"), height=20)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'), background='#3498db', foreground='white')
        style.configure("Treeview", font=('Helvetica', 10), rowheight=35)
        
        self.tree.heading("#0", text="S.No", anchor=W)
        self.tree.heading("ID", text="Patient ID", anchor=W)
        self.tree.heading("Name", text="Name", anchor=W)
        self.tree.heading("Sex", text="Sex", anchor=W)
        self.tree.heading("BG", text="Blood Group", anchor=W)
        self.tree.heading("DOB", text="DOB", anchor=W)
        self.tree.heading("Address", text="Address", anchor=W)
        self.tree.heading("Email", text="Email", anchor=W)
        
        self.tree.column("#0", width=60)
        self.tree.column("ID", width=100)
        self.tree.column("Name", width=180)
        self.tree.column("Sex", width=80)
        self.tree.column("BG", width=100)
        self.tree.column("DOB", width=120)
        self.tree.column("Address", width=250)
        self.tree.column("Email", width=200)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        
        vsb = ttk.Scrollbar(self.TreeFrame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.TreeFrame, orient="horizontal", command=self.tree.xscrollcommand)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        self.tree.bind('<Double-Button-1>', self.OnDoubleClick)
        self.LOAD_PATIENTS()
    
    def LOAD_PATIENTS(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = sqlite3.connect("HospitalDB.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PATIENT ORDER BY NAME")
            results = cursor.fetchall()
            
            if not results:
                tkinter.messagebox.showinfo("Information", "No patients found!")
            else:
                sno = 1
                for row in results:
                    self.tree.insert("", END, text=str(sno), values=(row[0], row[1], row[2], row[3], row[4], row[5], row[7]))
                    sno += 1
                tkinter.messagebox.showinfo("Success", f"Loaded {len(results)} patient(s)!")
            
            conn.close()
        except Exception as e:
            tkinter.messagebox.showerror("Database Error", f"Error: {str(e)}")
    
    def OnDoubleClick(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']
            details = f"""
╔═══════════════════════════════════════════╗
║       👤 PATIENT DETAILS                   ║
╚═══════════════════════════════════════════╝

🆔 Patient ID:   {values[1]}
👤 Name:         {values[2]}
🚹 Sex:          {values[3]}
🩸 Blood Group:  {values[4]}
📅 DOB:          {values[5]}
📍 Address:      {values[6]}
📧 Email:        {values[7]}

═══════════════════════════════════════════
            """
            tkinter.messagebox.showinfo("Patient Details", details)

# Medicine Management Class
class NurseMedicineMgmt:
    def __init__(self,master):
        self.master = master
        self.master.title("MEDICINE MANAGEMENT - NURSE DASHBOARD")
        self.master.geometry("1200x600+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        self.lblTitle = Label(self.frame,text = "💊 MEDICINE INVENTORY", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=20)
        
        self.InfoFrame = Frame(self.frame,width=800,height=300,relief="ridge",bg="powder blue",bd=20)
        self.InfoFrame.grid(row=1,column=0,pady=20)
        
        self.lblPatID = Label(self.InfoFrame,text="PATIENT ID",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblPatID.grid(row=0,column=0,pady=10)
        self.txtPatID = Entry(self.InfoFrame,font="Helvetica 14 bold",bd=2,width=30)
        self.txtPatID.grid(row=0,column=1,pady=10)
        
        self.lblMedName = Label(self.InfoFrame,text="MEDICINE NAME",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblMedName.grid(row=1,column=0,pady=10)
        self.txtMedName = Entry(self.InfoFrame,font="Helvetica 14 bold",bd=2,width=30)
        self.txtMedName.grid(row=1,column=1,pady=10)
        
        self.lblQty = Label(self.InfoFrame,text="QUANTITY",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblQty.grid(row=2,column=0,pady=10)
        self.txtQty = Entry(self.InfoFrame,font="Helvetica 14 bold",bd=2,width=30)
        self.txtQty.grid(row=2,column=1,pady=10)
        
        self.ButtonFrame = Frame(self.frame,width=800,height=100,relief="ridge",bg="cadet blue",bd=20)
        self.ButtonFrame.grid(row=2,column=0,pady=20)
        
        self.btnSave = Button(self.ButtonFrame,text = "💾 SAVE", width =15,font="Helvetica 14 bold",bg="green",fg="white",command=self.SAVE_MEDICINE)
        self.btnSave.grid(row=0,column=0,pady=10,padx=10)
        
        self.btnView = Button(self.ButtonFrame,text = "📋 VIEW ALL", width =15,font="Helvetica 14 bold",bg="blue",fg="white",command=self.VIEW_MEDICINES)
        self.btnView.grid(row=0,column=1,pady=10,padx=10)
    
    def SAVE_MEDICINE(self):
        pat_id = self.txtPatID.get()
        med_name = self.txtMedName.get()
        qty = self.txtQty.get()
        
        if not pat_id or not med_name:
            tkinter.messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            conn = sqlite3.connect("HospitalDB.db")
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO MEDICINE (PATIENT_ID, MEDICINE_NAME, M_COST, M_QTY) VALUES (?, ?, ?, ?)""",
                          (pat_id, med_name, 0, qty))
            conn.commit()
            tkinter.messagebox.showinfo("Success", "Medicine added successfully!")
            conn.close()
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Error: {str(e)}")
    
    def VIEW_MEDICINES(self):
        self.newWindow = Toplevel(self.master)
        self.app = ViewAllMedicines(self.newWindow)

class ViewAllMedicines:
    def __init__(self,master):
        self.master = master
        self.master.title("VIEW MEDICINES")
        self.master.geometry("1000x500+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        self.lblTitle = Label(self.frame,text = "💊 ALL MEDICINES", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,pady=20)
        
        self.TreeFrame = Frame(self.frame,width=900,height=400,relief="ridge",bg="white",bd=20)
        self.TreeFrame.grid(row=1,column=0,pady=10)
        
        self.tree = ttk.Treeview(self.TreeFrame, columns=("PatID", "MedName", "Cost", "Qty"), height=15)
        self.tree.heading("#0", text="S.No")
        self.tree.heading("PatID", text="Patient ID")
        self.tree.heading("MedName", text="Medicine Name")
        self.tree.heading("Cost", text="Cost")
        self.tree.heading("Qty", text="Quantity")
        
        self.tree.column("#0", width=60)
        self.tree.column("PatID", width=120)
        self.tree.column("MedName", width=250)
        self.tree.column("Cost", width=100)
        self.tree.column("Qty", width=100)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        
        try:
            conn = sqlite3.connect("HospitalDB.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM MEDICINE")
            results = cursor.fetchall()
            
            sno = 1
            for row in results:
                self.tree.insert("", END, text=str(sno), values=(row[0], row[1], row[2], row[3]))
                sno += 1
            
            conn.close()
        except Exception as e:
            tkinter.messagebox.showerror("Error", str(e))

# Doctor Schedule Class
class DoctorSchedule:
    def __init__(self,master):
        self.master = master
        self.master.title("DOCTOR SCHEDULE - NURSE DASHBOARD")
        self.master.geometry("1200x600+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        self.lblTitle = Label(self.frame,text = "📅 DOCTOR SCHEDULE MANAGEMENT", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=20)
        
        self.ScheduleFrame = Frame(self.frame,width=1100,height=400,relief="ridge",bg="white",bd=20)
        self.ScheduleFrame.grid(row=1,column=0,pady=20)
        
        # Sample schedule display
        schedule_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                    📅 TODAY'S DOCTOR SCHEDULE                        ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  🩺 Dr. John Smith      - Cardiology        - Room 301 - 9AM-5PM    ║
║  🩺 Dr. Emily Brown     - Neurology         - Room 302 - 10AM-6PM   ║
║  🩺 Dr. Michael Chen    - Orthopedics       - Room 303 - 8AM-4PM    ║
║  🩺 Dr. Sarah Johnson   - Pediatrics        - Room 304 - 9AM-5PM    ║
║  🩺 Dr. David Wilson    - Emergency         - ER Wing  - 24/7       ║
║  🩺 Dr. Lisa Anderson   - Dermatology       - Room 305 - 11AM-7PM   ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  📞 Emergency Contact: 555-0100                                      ║
║  🏥 Main Reception: 555-0101                                         ║
╚══════════════════════════════════════════════════════════════════════╝
        """
        
        self.lblSchedule = Label(self.ScheduleFrame,text=schedule_text,font="Courier 12",bg="white",justify=LEFT)
        self.lblSchedule.pack(pady=20)

# Patient Vitals Class
class PatientVitals:
    def __init__(self,master):
        self.master = master
        self.master.title("PATIENT VITALS - NURSE DASHBOARD")
        self.master.geometry("1200x600+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        self.lblTitle = Label(self.frame,text = "❤️ PATIENT VITALS MONITORING", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=20)
        
        self.VitalsFrame = Frame(self.frame,width=1100,height=400,relief="ridge",bg="white",bd=20)
        self.VitalsFrame.grid(row=1,column=0,pady=20)
        
        vitals_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                    ❤️ CURRENT PATIENT VITALS                         ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Patient: John Doe (ID: P001)                                       ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    ║
║  🫀 Blood Pressure: 120/80 mmHg                                     ║
║  💓 Heart Rate: 72 bpm                                              ║
║  🌡️  Temperature: 98.6°F                                            ║
║  💨 Respiratory Rate: 16 breaths/min                                ║
║  💉 Oxygen Saturation: 98%                                          ║
║                                                                      ║
║  Patient: Jane Smith (ID: P002)                                     ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    ║
║  🫀 Blood Pressure: 130/85 mmHg                                     ║
║  💓 Heart Rate: 80 bpm                                              ║
║  🌡️  Temperature: 99.1°F                                            ║
║  💨 Respiratory Rate: 18 breaths/min                                ║
║  💉 Oxygen Saturation: 96%                                          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
        """
        
        self.lblVitals = Label(self.VitalsFrame,text=vitals_text,font="Courier 12",bg="white",justify=LEFT)
        self.lblVitals.pack(pady=20)

# Ward Management Class
class WardManagement:
    def __init__(self,master):
        self.master = master
        self.master.title("WARD MANAGEMENT - NURSE DASHBOARD")
        self.master.geometry("1200x600+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        self.lblTitle = Label(self.frame,text = "🏥 WARD & ROOM MANAGEMENT", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=20)
        
        self.WardFrame = Frame(self.frame,width=1100,height=400,relief="ridge",bg="white",bd=20)
        self.WardFrame.grid(row=1,column=0,pady=20)
        
        ward_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                    🏥 WARD STATUS OVERVIEW                           ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  🛏️  Ward A - General Medicine                                      ║
║     Total Beds: 20 | Occupied: 15 | Available: 5                     ║
║     Nurses on Duty: 3                                                ║
║                                                                      ║
║  🛏️  Ward B - Surgical                                              ║
║     Total Beds: 15 | Occupied: 12 | Available: 3                     ║
║     Nurses on Duty: 2                                                ║
║                                                                      ║
║  🛏️  ICU - Intensive Care Unit                                      ║
║     Total Beds: 10 | Occupied: 8 | Available: 2                      ║
║     Nurses on Duty: 4                                                ║
║                                                                      ║
║  🛏️  Pediatric Ward                                                 ║
║     Total Beds: 12 | Occupied: 7 | Available: 5                      ║
║     Nurses on Duty: 2                                                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
        """
        
        self.lblWard = Label(self.WardFrame,text=ward_text,font="Courier 12",bg="white",justify=LEFT)
        self.lblWard.pack(pady=20)

# Nursing Notes Class
class NursingNotes:
    def __init__(self,master):
        self.master = master
        self.master.title("NURSING NOTES - NURSE DASHBOARD")
        self.master.geometry("1200x600+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        self.lblTitle = Label(self.frame,text = "📝 NURSING NOTES & OBSERVATIONS", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=20)
        
        self.NotesFrame = Frame(self.frame,width=1100,height=400,relief="ridge",bg="white",bd=20)
        self.NotesFrame.grid(row=1,column=0,pady=20)
        
        notes_text = """
╔══════════════════════════════════════════════════════════════════════╗
║                    📝 RECENT NURSING NOTES                           ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  [2026-03-25 08:30] Patient P001 - John Doe                         ║
║  - Vital signs stable                                               ║
║  - Medication administered on time                                  ║
║  - Patient reports feeling better                                   ║
║  - Continue monitoring                                              ║
║                                                                      ║
║  [2026-03-25 09:15] Patient P002 - Jane Smith                       ║
║  - BP slightly elevated (130/85)                                    ║
║  - Notified attending physician                                     ║
║  - Follow-up in 2 hours                                             ║
║                                                                      ║
║  [2026-03-25 10:00] Ward A Inspection                               ║
║  - All equipment functioning properly                               ║
║  - Emergency supplies checked and stocked                           ║
║  - Infection control protocols followed                             ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
        """
        
        self.lblNotes = Label(self.NotesFrame,text=notes_text,font="Courier 12",bg="white",justify=LEFT)
        self.lblNotes.pack(pady=20)

# Emergency Protocol Class
class EmergencyProtocol:
    def __init__(self,master):
        self.master = master
        self.master.title("EMERGENCY PROTOCOL - NURSE DASHBOARD")
        self.master.geometry("1200x600+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        self.lblTitle = Label(self.frame,text = "🚨 EMERGENCY PROTOCOLS", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=20)
        
        self.EmergencyFrame = Frame(self.frame,width=1100,height=400,relief="ridge",bg="white",bd=20)
        self.EmergencyFrame.grid(row=1,column=0,pady=20)
        
        emergency_text = """
╔══════════════════════════════════════════════════════════════════════╗
║              🚨 EMERGENCY CONTACTS & PROTOCOLS                       ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  📞 EMERGENCY NUMBERS:                                              ║
║     • Code Blue (Cardiac Arrest): Ext. 5555                         ║
║     • Rapid Response Team: Ext. 4444                                ║
║     • Emergency Department: Ext. 3333                               ║
║     • Security: Ext. 2222                                           ║
║     • Main Switchboard: 555-0100                                    ║
║                                                                      ║
║  🏥 KEY PERSONNEL:                                                  ║
║     • Chief of Staff: Dr. Robert Hayes - Ext. 1001                  ║
║     • Nursing Supervisor: Mary Johnson - Ext. 1002                  ║
║     • On-Call Administrator: Ext. 1003                              ║
║                                                                      ║
║  ⚡ QUICK ACTIONS:                                                   ║
║     1. Assess situation                                             ║
║     2. Call appropriate code                                        ║
║     3. Begin CPR if needed                                          ║
║     4. Prepare crash cart                                           ║
║     5. Document everything                                          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
        """
        
        self.lblEmergency = Label(self.EmergencyFrame,text=emergency_text,font="Courier 12",bg="white",justify=LEFT)
        self.lblEmergency.pack(pady=20)
