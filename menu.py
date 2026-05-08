from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from tkinter import font
import sqlite3
from patient_form import Patient
from room_form import Room
from employee_form import Employee
from appointment_form import Appointment
from billing_form import Billing
from ai_assistant import AIAssistant
from nurse_form import Nurse
from view_nurses import VIEW_ALL_NURSES

conn=sqlite3.connect("HospitalDB.db")

print("DATABASE CONNECTION SUCCESSFUL")

#Class For Menu    
class Menu:
    def __init__(self,master):
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("800x600+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
       
        self.lblTitle = Label(self.frame,text = "MAIN MENU", font="Helvetica 20 bold",bg="cadet blue")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=50)
        
        self.LoginFrame = Frame(self.frame,width=400,height=80,relief="ridge",bg="cadet blue",bd=20)
        self.LoginFrame.grid(row=1,column=0)
        #===========BUTTONS============= 
        self.button1 = Button(self.LoginFrame,text = "1.PATIENT REGISTRATION", width =30,font="Helvetica 14 bold",bg="cadet blue",command=self.Patient_Reg)       
        self.button1.grid(row=1,column=0,pady=10)
        
        self.button2 = Button(self.LoginFrame, text="2.ROOM ALLOCATION",width =30,font="Helvetica 14 bold",bg="cadet blue",command=self.Room_Allocation)
        self.button2.grid(row=3,column=0,pady=10)
        
        self.button3 = Button(self.LoginFrame, text="3.EMPLOYEE REGISTRATION",width =30,font="Helvetica 14 bold",bg="cadet blue",command=self.Employee_Reg)
        self.button3.grid(row=5,column=0,pady=10)
        
        self.button8 = Button(self.LoginFrame, text="💉 NURSE MANAGEMENT",width =30,font="Helvetica 14 bold",bg="#ff6b6b",fg="white",command=self.Nurse_Management)
        self.button8.grid(row=6,column=0,pady=10)
        
        self.button9 = Button(self.LoginFrame, text="📋 VIEW NURSES",width =30,font="Helvetica 14 bold",bg="purple",fg="white",command=self.View_Nurses)
        self.button9.grid(row=7,column=0,pady=10)
        
        self.button4 = Button(self.LoginFrame, text="4.BOOK APPOINTMENT",width =30,font="Helvetica 14 bold",bg="cadet blue",command=self.Appointment_Form)
        self.button4.grid(row=8,column=0,pady=10)
        
        self.button5 = Button(self.LoginFrame, text="5.PATIENT BILL",width =30,font="Helvetica 14 bold",bg="cadet blue",command=self.Billing_Form)
        self.button5.grid(row=9,column=0,pady=10)
        
        self.button7 = Button(self.LoginFrame, text="🤖 AI MEDICAL ASSISTANT",width =30,font="Helvetica 14 bold",bg="green",fg="white",command=self.AI_Assistant)
        self.button7.grid(row=10,column=0,pady=10)
        
        self.button6 = Button(self.LoginFrame, text="6.EXIT",width =30,font="Helvetica 14 bold",bg="cadet blue",command = self.Exit)
        self.button6.grid(row=11,column=0,pady=10)
        
    #Function to Exit Menu Window
    def Exit(self):
        self.master.destroy()

    
    #Function to open Patient Registration Window   
    def Patient_Reg(self):
        self.newWindow = Toplevel(self.master)
        self.app = Patient(self.newWindow)
        
    #Function to open Room Allocation Window   

    def Room_Allocation(self):
        self.newWindow = Toplevel(self.master)
        self.app = Room(self.newWindow)
        
    #Function to open Employee Registration Window 
    def Employee_Reg(self):
        self.newWindow = Toplevel(self.master)
        self.app = Employee(self.newWindow)
        
    #Function to open Appointment Window
    def Appointment_Form(self):
        self.newWindow = Toplevel(self.master)
        self.app = Appointment(self.newWindow)
        
    #Function to open Billing Window
    def Billing_Form(self):
        self.newWindow = Toplevel(self.master)
        self.app = Billing(self.newWindow)
    
    #Function to open AI Medical Assistant Window
    def AI_Assistant(self):
        self.newWindow = Toplevel(self.master)
        self.app = AIAssistant(self.newWindow)
    
    #Function to open Nurse Management Window
    def Nurse_Management(self):
        self.newWindow = Toplevel(self.master)
        self.app = Nurse(self.newWindow)
    
    #Function to open View Nurses Window
    def View_Nurses(self):
        self.newWindow = Toplevel(self.master)
        self.app = VIEW_ALL_NURSES(self.newWindow)


