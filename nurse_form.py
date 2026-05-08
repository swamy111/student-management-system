from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from tkinter import font
import sqlite3
import threading
from view_nurses import VIEW_ALL_NURSES

conn=sqlite3.connect("HospitalDB.db")
print("DATABASE CONNECTION SUCCESSFUL")

#Class for Nurse Management
class Nurse:
    def __init__(self,master):
        self.master = master
        self.master.title("NURSE MANAGEMENT - HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1500x700+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        # Attributes
        self.nurse_id=StringVar()
        self.nurse_name=StringVar()
        self.department=StringVar()
        self.shift=StringVar()
        self.phone=StringVar()
        self.email=StringVar()
        self.experience=StringVar()
        self.specialization=StringVar()
        
        # Title
        self.lblTitle = Label(self.frame,text = "💉 NURSE MANAGEMENT", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=30)
        
        # Info Frame
        self.InfoFrame = Frame(self.frame,width=800,height=400,relief="ridge",bg="powder blue",bd=20)
        self.InfoFrame.grid(row=1,column=0,pady=20)
        
        # Labels and Entries
        self.lblNurseID = Label(self.InfoFrame,text="NURSE ID",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblNurseID.grid(row=0,column=0,pady=10)
        self.txtNurseID = Entry(self.InfoFrame,font="Helvetica 14 bold",bd=2,textvariable=self.nurse_id,width=30)
        self.txtNurseID.grid(row=0,column=1,pady=10)
        
        self.lblName = Label(self.InfoFrame,text="NURSE NAME",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblName.grid(row=1,column=0,pady=10)
        self.txtName = Entry(self.InfoFrame,font="Helvetica 14 bold",bd=2,textvariable=self.nurse_name,width=30)
        self.txtName.grid(row=1,column=1,pady=10)
        
        self.lblDept = Label(self.InfoFrame,text="DEPARTMENT",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblDept.grid(row=2,column=0,pady=10)
        self.comboDept = ttk.Combobox(self.InfoFrame,font="Helvetica 14 bold",textvariable=self.department,width=28,state='readonly')
        self.comboDept['values'] = ("Emergency", "ICU", "General Ward", "Pediatrics", "Operation Theater", "Labor", "Outpatient")
        self.comboDept.grid(row=2,column=1,pady=10)
        
        self.lblShift = Label(self.InfoFrame,text="SHIFT",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblShift.grid(row=3,column=0,pady=10)
        self.comboShift = ttk.Combobox(self.InfoFrame,font="Helvetica 14 bold",textvariable=self.shift,width=28,state='readonly')
        self.comboShift['values'] = ("Morning (6AM-2PM)", "Afternoon (2PM-10PM)", "Night (10PM-6AM)", "12 Hours")
        self.comboShift.grid(row=3,column=1,pady=10)
        
        self.lblPhone = Label(self.InfoFrame,text="PHONE NUMBER",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblPhone.grid(row=4,column=0,pady=10)
        self.txtPhone = Entry(self.InfoFrame,font="Helvetica 14 bold",bd=2,textvariable=self.phone,width=30)
        self.txtPhone.grid(row=4,column=1,pady=10)
        
        self.lblEmail = Label(self.InfoFrame,text="EMAIL",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblEmail.grid(row=0,column=2,pady=10)
        self.txtEmail = Entry(self.InfoFrame,font="Helvetica 14 bold",bd=2,textvariable=self.email,width=30)
        self.txtEmail.grid(row=0,column=3,pady=10)
        
        selflblExp = Label(self.InfoFrame,text="EXPERIENCE (Years)",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblExp.grid(row=1,column=2,pady=10)
        self.txtExp = Entry(self.InfoFrame,font="Helvetica 14 bold",bd=2,textvariable=self.experience,width=30)
        self.txtExp.grid(row=1,column=3,pady=10)
        
        self.lblSpec = Label(self.InfoFrame,text="SPECIALIZATION",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblSpec.grid(row=2,column=2,pady=10)
        self.txtSpec = Entry(self.InfoFrame,font="Helvetica 14 bold",bd=2,textvariable=self.specialization,width=30)
        self.txtSpec.grid(row=2,column=3,pady=10)
        
        # Buttons Frame
        self.ButtonFrame = Frame(self.frame,width=800,height=100,relief="ridge",bg="cadet blue",bd=20)
        self.ButtonFrame.grid(row=2,column=0,pady=20)
        
        self.btnSave = Button(self.ButtonFrame,text = "💾 SAVE", width =15,font="Helvetica 14 bold",bg="green",fg="white",command=self.INSERT_NURSE)
        self.btnSave.grid(row=0,column=0,pady=10,padx=10)
        
        self.btnUpdate = Button(self.ButtonFrame,text = "🔄 UPDATE", width =15,font="Helvetica 14 bold",bg="blue",fg="white",command=self.UPDATE_NURSE)
        self.btnUpdate.grid(row=0,column=1,pady=10,padx=10)
        
        self.btnDelete = Button(self.ButtonFrame,text = "🗑️ DELETE", width =15,font="Helvetica 14 bold",bg="red",fg="white",command=self.DELETE_NURSE_DISPLAY)
        self.btnDelete.grid(row=0,column=2,pady=10,padx=10)
        
        self.btnSearch = Button(self.ButtonFrame,text = "🔍 SEARCH", width =15,font="Helvetica 14 bold",bg="orange",fg="white",command=self.SEARCH_NURSE_DISPLAY)
        self.btnSearch.grid(row=0,column=3,pady=10,padx=10)
        
        self.btnExit = Button(self.ButtonFrame,text = "❌ EXIT", width =15,font="Helvetica 14 bold",bg="grey",fg="white",command=self.Exit)
        self.btnExit.grid(row=0,column=4,pady=10,padx=10)
        
        self.btnViewAll = Button(self.ButtonFrame,text = "📋 VIEW ALL NURSES", width =20,font="Helvetica 14 bold",bg="purple",fg="white",command=self.VIEW_ALL_NURSES)
        self.btnViewAll.grid(row=0,column=5,pady=10,padx=10)
    
    # Function to insert nurse data
    def INSERT_NURSE(self):
        nid = self.nurse_id.get().strip()
        name = self.nurse_name.get().strip()
        dept = self.department.get().strip()
        shift = self.shift.get().strip()
        phone = self.phone.get().strip()
        email = self.email.get().strip()
        exp = self.experience.get().strip()
        spec = self.specialization.get().strip()
        
        if not nid or not name:
            tkinter.messagebox.showerror("Error", "Nurse ID and Name are required!")
            return
        
        try:
            conn = sqlite3.connect("HospitalDB.db")
            cursor = conn.cursor()
            
            # Check if nurse already exists
            cursor.execute("SELECT * FROM nurse WHERE NURSE_ID=?", (nid,))
            existing = cursor.fetchone()
            
            if existing:
                tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "NURSE ALREADY EXISTS")
            else:
                cursor.execute("""INSERT INTO nurse 
                                (NURSE_ID, NAME, DEPARTMENT, SHIFT, PHONE, EMAIL, EXPERIENCE, SPECIALIZATION) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                              (nid, name, dept, shift, phone, email, exp, spec))
                conn.commit()
                tkinter.messagebox.showinfo("HOSPITAL DATABASE SYSTEM", "NURSE ADDED SUCCESSFULLY")
                self.clear_form()
            
            conn.close()
        except Exception as e:
            tkinter.messagebox.showerror("Database Error", f"Error: {str(e)}")
    
    # Function to update nurse data
    def UPDATE_NURSE(self):
        nid = self.nurse_id.get().strip()
        name = self.nurse_name.get().strip()
        dept = self.department.get().strip()
        shift = self.shift.get().strip()
        phone = self.phone.get().strip()
        email = self.email.get().strip()
        exp = self.experience.get().strip()
        spec = self.specialization.get().strip()
        
        if not nid:
            tkinter.messagebox.showerror("Error", "Nurse ID is required!")
            return
        
        try:
            conn = sqlite3.connect("HospitalDB.db")
            cursor = conn.cursor()
            
            cursor.execute("""UPDATE nurse SET 
                            NAME=?, DEPARTMENT=?, SHIFT=?, PHONE=?, EMAIL=?, EXPERIENCE=?, SPECIALIZATION=?
                            WHERE NURSE_ID=?""",
                          (name, dept, shift, phone, email, exp, spec, nid))
            conn.commit()
            
            if cursor.rowcount > 0:
                tkinter.messagebox.showinfo("HOSPITAL DATABASE SYSTEM", "NURSE DATA UPDATED SUCCESSFULLY")
                self.clear_form()
            else:
                tkinter.messagebox.showerror("Error", "Nurse not found!")
            
            conn.close()
        except Exception as e:
            tkinter.messagebox.showerror("Database Error", f"Error: {str(e)}")
    
    # Function to delete nurse
    def DELETE_NURSE_DISPLAY(self):
        self.newWindow = Toplevel(self.master)
        self.app = DEL_NURSE(self.newWindow)
    
    # Function to search nurse
    def SEARCH_NURSE_DISPLAY(self):
        self.newWindow = Toplevel(self.master)
        self.app = SEA_NURSE(self.newWindow)
    
    # Function to view all nurses
    def VIEW_ALL_NURSES(self):
        self.newWindow = Toplevel(self.master)
        self.app = VIEW_ALL_NURSES(self.newWindow)
    
    # Function to clear form
    def clear_form(self):
        self.nurse_id.set("")
        self.nurse_name.set("")
        self.department.set("")
        self.shift.set("")
        self.phone.set("")
        self.email.set("")
        self.experience.set("")
        self.specialization.set("")
    
    # Function to Exit
    def Exit(self):
        self.master.destroy()

# Class for Delete Nurse
class DEL_NURSE:
    def __init__(self,master):
        self.master = master
        self.master.title("DELETE NURSE - HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("800x400+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        self.del_id = StringVar()
        
        self.lblTitle = Label(self.frame,text = "🗑️ DELETE NURSE", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=30)
        
        self.LoginFrame = Frame(self.frame,width=400,height=80,relief="ridge",bg="powder blue",bd=20)
        self.LoginFrame.grid(row=1,column=0)
        
        self.lblNurseID = Label(self.LoginFrame,text="ENTER NURSE ID TO DELETE",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblNurseID.grid(row=0,column=0,pady=20)
        
        self.txtNurseID = Entry(self.LoginFrame,font="Helvetica 14 bold",bd=2,textvariable=self.del_id,width=30)
        self.txtNurseID.grid(row=0,column=1,pady=20)
        
        self.btnDelete = Button(self.LoginFrame,text = "🗑️ DELETE", width =20,font="Helvetica 14 bold",bg="red",fg="white",command=self.DELETE_NURSE)
        self.btnDelete.grid(row=1,column=1,pady=20)
    
    def DELETE_NURSE(self):
        nid = self.del_id.get().strip()
        
        if not nid:
            tkinter.messagebox.showerror("Error", "Nurse ID is required!")
            return
        
        try:
            conn = sqlite3.connect("HospitalDB.db")
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM nurse WHERE NURSE_ID=?", (nid,))
            existing = cursor.fetchone()
            
            if not existing:
                tkinter.messagebox.showerror("HOSPITAL DATABASE SYSTEM", "NURSE NOT FOUND")
            else:
                cursor.execute("DELETE FROM nurse WHERE NURSE_ID=?", (nid,))
                conn.commit()
                tkinter.messagebox.showinfo("HOSPITAL DATABASE SYSTEM", "NURSE DELETED SUCCESSFULLY")
                self.master.destroy()
            
            conn.close()
        except Exception as e:
            tkinter.messagebox.showerror("Database Error", f"Error: {str(e)}")

# Class for Search Nurse
class SEA_NURSE:
    def __init__(self,master):
        self.master = master
        self.master.title("SEARCH NURSE - HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1200x600+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        self.search_id = StringVar()
        
        self.lblTitle = Label(self.frame,text = "🔍 SEARCH NURSE", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=20)
        
        self.LoginFrame = Frame(self.frame,width=600,height=100,relief="ridge",bg="powder blue",bd=20)
        self.LoginFrame.grid(row=1,column=0)
        
        self.lblSearch = Label(self.LoginFrame,text="ENTER NURSE ID OR NAME",font="Helvetica 14 bold",bg="powder blue",bd=15)
        self.lblSearch.grid(row=0,column=0,pady=10)
        
        self.txtSearch = Entry(self.LoginFrame,font="Helvetica 14 bold",bd=2,textvariable=self.search_id,width=40)
        self.txtSearch.grid(row=0,column=1,pady=10)
        
        self.btnSearch = Button(self.LoginFrame,text = "🔍 SEARCH", width =20,font="Helvetica 14 bold",bg="orange",fg="white",command=self.SEARCH_NURSE)
        self.btnSearch.grid(row=1,column=1,pady=10)
        
        # Result Treeview
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name", "Department", "Shift", "Phone", "Email", "Exp", "Spec"), height=15)
        self.tree.heading("#0", text="S.No")
        self.tree.heading("ID", text="Nurse ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Shift", text="Shift")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Exp", text="Experience")
        self.tree.heading("Spec", text="Specialization")
        
        self.tree.column("#0", width=50)
        self.tree.column("ID", width=100)
        self.tree.column("Name", width=150)
        self.tree.column("Department", width=120)
        self.tree.column("Shift", width=120)
        self.tree.column("Phone", width=100)
        self.tree.column("Email", width=150)
        self.tree.column("Exp", width=80)
        self.tree.column("Spec", width=120)
        
        self.tree.grid(row=2,column=0,pady=20)
    
    def SEARCH_NURSE(self):
        search_term = self.search_id.get().strip()
        
        if not search_term:
            tkinter.messagebox.showerror("Error", "Please enter search term!")
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = sqlite3.connect("HospitalDB.db")
            cursor = conn.cursor()
            
            # Search by ID or Name
            cursor.execute("""SELECT * FROM nurse WHERE NURSE_ID LIKE ? OR NAME LIKE ?""", 
                          (f'%{search_term}%', f'%{search_term}%'))
            results = cursor.fetchall()
            
            if not results:
                tkinter.messagebox.showinfo("Result", "No nurses found matching your search!")
            else:
                sno = 1
                for row in results:
                    self.tree.insert("", END, text=str(sno), values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                    sno += 1
            
            conn.close()
        except Exception as e:
            tkinter.messagebox.showerror("Database Error", f"Error: {str(e)}")
