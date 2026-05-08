from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from tkinter import font
import sqlite3

from menu import Menu

def main():
    root = Tk()
    app = MainWindow(root)
    root.mainloop()
#MAIN WINDOW FOR LOG IN
class MainWindow:
    # constructor
    def __init__(self,master):
        # public data mambers
        self.master = master
        self.master.title("HOSPITAL MANAGEMENT SYSTEM - LOGIN")
        self.master.geometry("1200x700+0+0")
        
        # Modern gradient background
        self.master.config(bg="#1e3c72")
        
        # Create canvas for gradient effect
        self.canvas = Canvas(master, width=1200, height=700, bg="#1e3c72")
        self.canvas.pack(fill=BOTH, expand=True)
        
        # Create gradient background
        for i in range(50):
            color_val = int(30 + (i * 0.6))
            self.canvas.create_rectangle(0, i*14, 1200, (i+1)*14, 
                                        fill=f"#{color_val:02x}{40+i:02x}{80+i:02x}", outline="")
        
        # Add decorative circles
        for i in range(10):
            x = (i * 120) % 1200
            y = (i * 70) % 700
            self.canvas.create_oval(x, y, x+100, y+100, fill="#ffffff", outline="", tags="deco")
            self.canvas.itemconfig("deco", stipple='gray25')
        
        # Main frame with modern design
        self.frame = Frame(self.canvas, bg="white", bd=0, relief=FLAT)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=900, height=550)
        
        # Shadow effect
        self.shadow = Frame(self.canvas, bg="#000000", bd=0)
        self.shadow.place(relx=0.5, rely=0.5, anchor=CENTER, width=890, height=540)
        
        # Left side - Welcome panel
        self.leftPanel = Frame(self.frame, bg="#667eea", width=400, relief=RIDGE, bd=0)
        self.leftPanel.place(x=0, y=0, height=550)
        
        # Gradient canvas for left panel
        self.leftCanvas = Canvas(self.leftPanel, width=400, height=550, bg="#667eea")
        self.leftCanvas.pack(fill=BOTH, expand=True)
        
        # Create gradient
        for i in range(55):
            color_val = int(102 + (i * 0.5))
            color_mid = min(255, int(66 + i))
            self.leftCanvas.create_rectangle(0, i*10, 400, (i+1)*10, 
                                            fill=f"#{color_val:02x}{color_mid:02x}ea", outline="")
        
        # Hospital icon/emoji on left panel
        self.leftCanvas.create_text(200, 150, text="🏥", font=("Arial", 80), fill="white")
        self.leftCanvas.create_text(200, 250, text="HOSPITAL", font=("Arial Bold", 28, "bold"), 
                                   fill="white", justify=CENTER)
        self.leftCanvas.create_text(200, 285, text="MANAGEMENT", font=("Arial Bold", 28, "bold"), 
                                   fill="white", justify=CENTER)
        self.leftCanvas.create_text(200, 320, text="SYSTEM", font=("Arial Bold", 28, "bold"), 
                                   fill="white", justify=CENTER)
        self.leftCanvas.create_text(200, 380, text="Advanced Healthcare Solutions", 
                                   font=("Arial", 14, "italic"), fill="white")
        self.leftCanvas.create_text(200, 420, text="━━━━━━━━━━━━━━━━━━━━━━━", 
                                   font=("Arial", 12), fill="white")
        self.leftCanvas.create_text(200, 460, text="Secure • Reliable • Efficient", 
                                   font=("Arial", 12, "bold"), fill="white")
        
        # Right side - Login form
        self.rightPanel = Frame(self.frame, bg="white", width=500, relief=FLAT)
        self.rightPanel.place(x=400, y=0, height=550)
        
        self.Username = StringVar()
        self.Password = StringVar()
        
        # Title
        self.lblTitle = Label(self.rightPanel, text="Welcome Back!", 
                             font=("Helvetica", 24, "bold"), bg="white", fg="#1e3c72")
        self.lblTitle.place(x=50, y=40)
        
        self.lblSubtitle = Label(self.rightPanel, text="Please login to continue", 
                                font=("Helvetica", 12), bg="white", fg="#666")
        self.lblSubtitle.place(x=50, y=75)
        
        # Login Frame
        self.LoginFrame = Frame(self.rightPanel, bg="white", bd=0)
        self.LoginFrame.place(x=50, y=120, width=400)
        
        # Username field with icon
        self.lblUsernameIcon = Label(self.LoginFrame, text="👤", font=("Arial", 16), 
                                    bg="white", fg="#667eea")
        self.lblUsernameIcon.grid(row=0, column=0, padx=10, pady=15, sticky=W)
        
        self.lblUsername = Label(self.LoginFrame, text="Username / Email", 
                                font=("Helvetica", 12, "bold"), bg="white", fg="#333")
        self.lblUsername.grid(row=1, column=0, padx=10, pady=0, sticky=W)
        
        self.txtUsername = Entry(self.LoginFrame, font=("Helvetica", 14), 
                                textvariable=self.Username, bd=0, bg="#f5f5f5", 
                                relief=FLAT, fg="#333", insertbackground="#667eea")
        self.txtUsername.grid(row=2, column=0, padx=0, pady=10, sticky=EW)
        
        # Username underline
        self.usernameLine = Canvas(self.LoginFrame, width=380, height=2, bg="#667eea", highlightthickness=0)
        self.usernameLine.grid(row=3, column=0, padx=0, pady=0)
        
        # Password field with icon
        self.lblPasswordIcon = Label(self.LoginFrame, text="🔒", font=("Arial", 16), 
                                    bg="white", fg="#667eea")
        self.lblPasswordIcon.grid(row=4, column=0, padx=10, pady=15, sticky=W)
        
        self.lblPassword = Label(self.LoginFrame, text="Password", 
                                font=("Helvetica", 12, "bold"), bg="white", fg="#333")
        self.lblPassword.grid(row=5, column=0, padx=10, pady=0, sticky=W)
        
        self.txtPassword = Entry(self.LoginFrame, font=("Helvetica", 14), 
                                show="•", textvariable=self.Password, bd=0, 
                                bg="#f5f5f5", relief=FLAT, fg="#333", insertbackground="#667eea")
        self.txtPassword.grid(row=6, column=0, padx=0, pady=10, sticky=EW)
        
        # Password underline
        self.passwordLine = Canvas(self.LoginFrame, width=380, height=2, bg="#667eea", highlightthickness=0)
        self.passwordLine.grid(row=7, column=0, padx=0, pady=0)
        
        # Buttons Frame
        self.LoginFrame2 = Frame(self.rightPanel, bg="white", bd=0)
        self.LoginFrame2.place(x=50, y=320, width=400)
        
        # Login button with gradient
        self.btnLogin = Button(self.LoginFrame2, text="LOGIN", 
                              font=("Helvetica", 14, "bold"), width=25, 
                              bg="#667eea", fg="white", bd=0, 
                              activebackground="#764ba2", activeforeground="white",
                              cursor="hand2", command=self.Login_system,
                              relief=RAISED, overrelief=SOLID)
        self.btnLogin.grid(row=0, column=0, pady=10)
        
        # Exit button
        self.btnExit = Button(self.LoginFrame2, text="EXIT", 
                             font=("Helvetica", 12), width=25, 
                             bg="#e0e0e0", fg="#333", bd=0, 
                             activebackground="#d0d0d0", activeforeground="#000",
                             cursor="hand2", command=self.Exit,
                             relief=RAISED, overrelief=SOLID)
        self.btnExit.grid(row=1, column=0, pady=5)
        
        # Footer
        self.footerLabel = Label(self.rightPanel, text="© 2026 Hospital Management System", 
                                font=("Helvetica", 9), bg="white", fg="#999")
        self.footerLabel.place(x=50, y=500)
    # public member function  
    #Function for LOGIN
    def Login_system(self):
        username = self.Username.get().strip()
        password = self.Password.get()
        
        if not username or not password:
            tkinter.messagebox.showerror("Login Error", "Please enter both username and password")
            return
        
        # Check credentials against database
        try:
            conn = sqlite3.connect("HospitalDB.db")
            cursor = conn.cursor()
            
            # Check in employee table
            cursor.execute("SELECT EMP_ID, EMP_NAME FROM employee WHERE EMP_ID=? AND SAL=?", 
                          (username, password))
            emp_result = cursor.fetchone()
            
            # Check admin credentials
            admin_login = (username == 'admin' and password == 'admin123')
            
            conn.close()
            
            if emp_result or admin_login:
                user_name = emp_result[1] if emp_result else "Administrator"
                tkinter.messagebox.showinfo("Login Successful", 
                                           f"Welcome, {user_name}!")
                self.newWindow = Toplevel(self.master)
                self.app = Menu(self.newWindow)
            else:
                tkinter.messagebox.showerror("Login Failed", 
                                            "Invalid username or password.\nPlease try again.")
        except Exception as e:
            tkinter.messagebox.showerror("Database Error", f"Error: {str(e)}")
    #Function for Exit
    def Exit(self):
        self.master.destroy()




if __name__ == "__main__":
    main()
