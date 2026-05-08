from tkinter import *
import tkinter.messagebox
from tkinter import ttk
import sqlite3

# Class for View All Nurses
class VIEW_ALL_NURSES:
    def __init__(self,master):
        self.master = master
        self.master.title("VIEW ALL NURSES - HOSPITAL MANAGEMENT SYSTEM")
        self.master.geometry("1400x700+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master,bg="cadet blue")
        self.frame.pack()
        
        self.lblTitle = Label(self.frame,text = "📋 VIEW ALL NURSES", font="Helvetica 20 bold",bg="cadet blue", fg="white")
        self.lblTitle.grid(row =0 ,column = 0,columnspan=2,pady=20)
        
        # Stats Frame
        self.StatsFrame = Frame(self.frame,width=1300,height=80,relief="ridge",bg="powder blue",bd=20)
        self.StatsFrame.grid(row=1,column=0,pady=10)
        
        self.lblTotal = Label(self.StatsFrame,text="TOTAL NURSES:",font="Helvetica 16 bold",bg="powder blue",fg="#2c3e50")
        self.lblTotal.grid(row=0,column=0,padx=20)
        
        self.lblTotalCount = Label(self.StatsFrame,text="0",font="Helvetica 20 bold",bg="powder blue",fg="#ff6b6b")
        self.lblTotalCount.grid(row=0,column=1,padx=10)
        
        # Refresh button
        self.btnRefresh = Button(self.StatsFrame,text="🔄 REFRESH",font="Helvetica 14 bold",bg="#11998e",fg="white",command=self.LOAD_NURSES)
        self.btnRefresh.grid(row=0,column=2,padx=20)
        
        # Treeview Frame
        self.TreeFrame = Frame(self.frame,width=1300,height=500,relief="ridge",bg="white",bd=20)
        self.TreeFrame.grid(row=2,column=0,pady=10)
        
        # Create Treeview with scrollbar
        self.tree = ttk.Treeview(self.TreeFrame, columns=("ID", "Name", "Dept", "Shift", "Phone", "Email", "Exp", "Spec"), height=20)
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'), background='#ff6b6b', foreground='white')
        style.configure("Treeview", font=('Helvetica', 10), rowheight=35)
        
        # Define headings
        self.tree.heading("#0", text="S.No", anchor=W)
        self.tree.heading("ID", text="Nurse ID", anchor=W)
        self.tree.heading("Name", text="Name", anchor=W)
        self.tree.heading("Dept", text="Department", anchor=W)
        self.tree.heading("Shift", text="Shift", anchor=W)
        self.tree.heading("Phone", text="Phone", anchor=W)
        self.tree.heading("Email", text="Email", anchor=W)
        self.tree.heading("Exp", text="Exp (Years)", anchor=W)
        self.tree.heading("Spec", text="Specialization", anchor=W)
        
        # Define columns
        self.tree.column("#0", width=60, minwidth=60, stretch=False)
        self.tree.column("ID", width=100, minwidth=100)
        self.tree.column("Name", width=180, minwidth=180)
        self.tree.column("Dept", width=120, minwidth=120)
        self.tree.column("Shift", width=140, minwidth=140)
        self.tree.column("Phone", width=120, minwidth=120)
        self.tree.column("Email", width=200, minwidth=200)
        self.tree.column("Exp", width=100, minwidth=100)
        self.tree.column("Spec", width=150, minwidth=150)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(self.TreeFrame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.TreeFrame, orient="horizontal", command=self.tree.xscrollcommand)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        self.TreeFrame.grid_rowconfigure(0, weight=1)
        self.TreeFrame.grid_columnconfigure(0, weight=1)
        
        # Bind double click to show details
        self.tree.bind('<Double-Button-1>', self.OnDoubleClick)
        
        # Load data
        self.LOAD_NURSES()
    
    def LOAD_NURSES(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = sqlite3.connect("HospitalDB.db")
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM nurse ORDER BY NAME")
            results = cursor.fetchall()
            
            # Update total count
            total = len(results)
            self.lblTotalCount.config(text=str(total))
            
            if not results:
                tkinter.messagebox.showinfo("Information", "No nurses found in the database!")
            else:
                sno = 1
                for row in results:
                    self.tree.insert("", END, text=str(sno), 
                                   values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                    sno += 1
                
                tkinter.messagebox.showinfo("Success", f"Loaded {total} nurse(s) from database!")
            
            conn.close()
        except Exception as e:
            tkinter.messagebox.showerror("Database Error", f"Error: {str(e)}")
    
    def OnDoubleClick(self, event):
        # Get selected item
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']
            
            # Show details in message box
            details = f"""
╔═══════════════════════════════════════════╗
║       💉 NURSE DETAILS                     ║
╚═══════════════════════════════════════════╝

🆔 Nurse ID:     {values[1]}
👤 Name:         {values[2]}
🏥 Department:   {values[3]}
⏰ Shift:        {values[4]}
📞 Phone:        {values[5]}
📧 Email:        {values[6]}
💼 Experience:   {values[7]} years
🎯 Specialization: {values[8]}

═══════════════════════════════════════════
            """
            tkinter.messagebox.showinfo("Nurse Details", details)
