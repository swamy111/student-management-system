# 🏥 Hospital Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)](https://www.sqlite.org/)
[![Tkinter](https://img.shields.io/badge/UI-Tkinter-yellow.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Demo](https://img.shields.io/badge/Live-Demo-brightgreen.svg)](https://gayathri1462.github.io/Hospital-Management-System/)

> A comprehensive, full-featured Hospital Management System with both **Desktop (Tkinter)** and **Web (Flask)** interfaces. This system streamlines hospital operations including patient registration, appointment scheduling, room allocation, employee management, billing, and nursing staff coordination.

🌐 **[👉 VIEW LIVE DEMO](https://gayathri1462.github.io/Hospital-Management-System/)**

---

## 📋 Table of Contents

- [Purpose](#-purpose)
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Screenshots & Output](#-screenshots--output)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Purpose

The Hospital Management System is designed to **computerize the Front Office Management of Hospitals** by developing software that is:
- ✅ **User-friendly** - Intuitive interface for staff at all levels
- ✅ **Simple** - Easy to navigate and operate
- ✅ **Fast** - Quick data processing and retrieval
- ✅ **Cost-effective** - Open-source technologies, zero licensing costs

The system manages:
- Patient information collection and diagnosis details
- Appointment scheduling and tracking
- Room allocation and availability
- Employee and nurse management
- Billing and financial records
- Medical inventory and protocols

**Access Control**: Secure login system with role-based access for administrators and receptionists. Only authorized personnel can add/modify data. All data is well-protected with secure authentication.

---

## ✨ Features

### 🔐 Authentication & Security
- Secure username/password login system
- Role-based access control (Admin, Receptionist, Nurse)
- Session management and data protection

### 👥 Patient Management
- Patient registration with complete medical history
- Search, update, and delete patient records
- Contact information management (primary & alternate)
- Blood group, DOB, and address tracking

### 📅 Appointment System
- Book appointments with doctors
- Search and filter appointments by date/patient
- Cancel and reschedule appointments
- Appointment status tracking

### 🏠 Room Allocation
- Real-time room availability checking
- Room type management (General, ICU, Private, etc.)
- Patient-room assignment and tracking
- Room status updates (Occupied, Available, Maintenance)

### 👨‍⚕️ Employee & Nurse Management
- Employee registration and profile management
- Designation, salary, and experience tracking
- Nurse dashboard with specialized tools
- Nurse scheduling and assignment

### 💰 Billing & Finance
- Automated bill generation
- Treatment cost calculation
- Discharge date tracking
- Payment status management
- Detailed billing reports

### 💊 Medical Features
- Treatment tracking with codes and costs
- Medicine management system
- Emergency protocol management
- Medical history records

### 🤖 AI Integration (Optional)
- AI-powered medical assistant
- Intelligent diagnosis support
- Smart appointment recommendations

### 🌐 Dual Interface
- **Desktop App**: Native Tkinter-based GUI
- **Web Portal**: Modern Flask-based responsive web interface
- Cross-platform compatibility (Windows, macOS, Linux)

---

## 🛠️ Technologies Used

### **Backend Technologies**
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **Flask** | 3.0.0 | Web framework for RESTful API |
| **SQLite** | 3 | Lightweight relational database |
| **Tkinter** | Built-in | Desktop GUI framework |

### **Frontend Technologies (Web Interface)**
| Technology | Purpose |
|------------|---------|
| **HTML5/CSS3** | Web page structure and styling |
| **JavaScript** | Client-side interactivity |
| **Font Awesome 6.4** | Icon library |
| **Google Fonts (Poppins)** | Typography |
| **CSS3 Animations** | Modern UI effects |

### **Development Tools**
| Tool | Purpose |
|------|---------|
| **DB Browser for SQLite** | Database management and visualization |
| **Git** | Version control |
| **GitHub** | Code hosting and collaboration |

### **System Architecture**
```
┌─────────────────────────────────────────────┐
│           USER INTERFACES                   │
│  ┌──────────────┐    ┌──────────────────┐   │
│  │ Desktop App  │    │   Web Browser    │   │
│  │  (Tkinter)   │    │  (Flask/HTML5)   │   │
│  └──────┬───────┘    └────────┬─────────┘   │
└─────────┼─────────────────────┼─────────────┘
          │                     │
          └──────────┬──────────┘
                     │
          ┌──────────▼──────────┐
          │   Flask Backend     │
          │   (app.py)          │
          │   - RESTful APIs    │
          │   - Route Handling  │
          │   - Business Logic  │
          └──────────┬──────────┘
                     │
          ┌──────────▼──────────┐
          │   SQLite Database   │
          │   (HospitalDB.db)   │
          │   - Patient Data    │
          │   - Appointments    │
          │   - Billing Records │
          └─────────────────────┘
```

---

## 📦 Installation

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/gayathri1462/Hospital-Management-System.git
cd Hospital-Management-System
```

### **Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 3: Initialize Database**
```bash
python setup_database.py
```

This will create the `HospitalDB.db` SQLite database with all required tables.

---

## 🎬 Quick Demo

Want to see it in action without installing? 

👉 **[View Interactive Demo Here](https://gayathri1462.github.io/Hospital-Management-System/)**

The demo includes:
- ✅ Full screenshot gallery
- ✅ Feature walkthrough
- ✅ Technology stack overview
- ✅ Quick start guide

---

## 🚀 Usage

### **Option 1: Web Interface (Recommended)**

1. **Start the Flask Server**:
```bash
python app.py
```

2. **Open Browser**:
   Navigate to: `http://localhost:5000`

3. **Login**:
   - Username: `admin`
   - Password: `admin`

### **Option 2: Desktop Application**

**On macOS/Linux**:
```bash
python login.py
```
Or double-click: `launch_app.command`

**On Windows**:
```bash
python login.py
```
Or double-click: `Hospital_System.bat`

### **Option 3: Nurse Portal**

**On macOS/Linux**:
```bash
python nurse_portal.py
```
Or double-click: `nurse_launcher.command`

---

## 📸 Screenshots & Output

### 🔐 Login Screen
**Successful Login**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/login-1.jpg?raw=true" width="600" height="400">

**Invalid Credentials**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/login-2.jpg?raw=true" width="600" height="400">

### 🏠 Main Dashboard
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/menu.jpg?raw=true" width="600" height="600">

### 👥 Patient Registration

**Submit New Patient**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/pat-reg-1.jpg?raw=true" width="800" height="400">

**Update Patient Details**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/pat-reg-2.jpg?raw=true" width="800" height="400">

**Search Patients**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/pat-reg-3.jpg?raw=true" width="800" height="400">

**Delete Patient Record**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/pat-reg-4.jpg?raw=true" width="800" height="400">

### 🏠 Room Allocation

**Allocate Room**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/room-alloc-1.jpg?raw=true" width="800" height="400">

**Update Room Details**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/room-alloc-2.jpg?raw=true" width="800" height="400">

**View Room Information**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/room-alloc-3.jpg?raw=true" width="800" height="400">

### 👨‍⚕️ Employee Registration

**Save Employee**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/emp-reg-1.jpg?raw=true" width="800" height="400">

**Delete Employee**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/emp-reg-2.jpg?raw=true" width="800" height="400">

### 📅 Appointment Booking

**Book Appointment**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/book-app-1.jpg?raw=true" width="800" height="400">

**Delete Appointment**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/book-app-2.jpg?raw=true" width="800" height="400">

**Search Appointments**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/book-app-3.jpg?raw=true" width="800" height="400">

### 💰 Patient Billing

**Update Patient Data**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/pat-bill-1.jpg?raw=true" width="800" height="400">

**Update Discharge Date**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/pat-bill-2.jpg?raw=true" width="800" height="400">

**Generate Bill**:
<img src="https://github.com/gayathri1462/Hospital-Management-System/blob/main/Output%20images/pat-bill-3.jpg?raw=true" width="800" height="400">

---

## 📁 Project Structure

```
Hospital-Management-System/
│
├── 📂 Core Application Files
│   ├── app.py                 # Flask web application (Main web server)
│   ├── login.py               # Desktop login interface
│   ├── menu.py                # Main menu system
│   ├── database.py            # Database initialization and schema
│   └── setup_database.py      # Database setup script
│
├── 📂 Management Modules
│   ├── patient_form.py        # Patient registration & CRUD operations
│   ├── employee_form.py       # Employee management system
│   ├── nurse_form.py          # Nurse registration & management
│   ├── nurse_dashboard.py     # Nurse dashboard with specialized tools
│   ├── nurse_portal.py        # Nurse portal entry point
│   ├── view_nurses.py         # Nurse list viewer
│   ├── appointment_form.py    # Appointment scheduling system
│   ├── room_form.py           # Room allocation management
│   └── billing_form.py        # Billing & invoice generation
│
├── 📂 Advanced Features
│   ├── ai_assistant.py        # AI-powered medical assistant
│   ├── medical_api.py         # Medical API integration
│   └── test_ai.py             # AI feature testing
│
├── 📂 Launchers & Scripts
│   ├── Hospital_System.bat    # Windows batch launcher
│   ├── Hospital_System.command # macOS/Linux launcher
│   ├── launch_app.command     # Quick app launcher (macOS)
│   └── nurse_launcher.command # Nurse portal launcher (macOS)
│
├── 📂 Documentation
│   ├── README.md              # Project documentation
│   ├── AI_FEATURES_SUMMARY.txt # AI features overview
│   ├── AI_INTEGRATION_GUIDE.md # AI integration guide
│   ├── DEPLOYMENT_GUIDE.md    # Deployment instructions
│   └── FIXES_APPLIED.txt      # Bug fixes changelog
│
├── 📂 Deployment
│   └── HospitalApp.app/       # macOS application bundle
│       ├── Contents/MacOS/HospitalApp
│       └── Contents/Info.plist
│
├── HospitalDB.db              # SQLite database (auto-generated)
└── requirements.txt           # Python dependencies
```

---

## 🗄️ Database Schema

### **Main Tables**

#### **PATIENT**
| Column | Type | Description |
|--------|------|-------------|
| PATIENT_ID | INT (PK) | Unique patient identifier |
| NAME | VARCHAR(20) | Patient full name |
| SEX | VARCHAR(10) | Gender |
| BLOOD_GROUP | VARCHAR(5) | Blood type |
| DOB | DATE | Date of birth |
| ADDRESS | VARCHAR(100) | Residential address |
| CONSULT_TEAM | VARCHAR(50) | Assigned medical team |
| EMAIL | VARCHAR(20) | Email address |

#### **CONTACT_NO**
| Column | Type | Description |
|--------|------|-------------|
| PATIENT_ID | INT (PK, FK) | References PATIENT |
| CONTACTNO | INT(15) | Primary contact number |
| ALT_CONTACT | INT(15) | Alternate contact number |

#### **EMPLOYEE**
| Column | Type | Description |
|--------|------|-------------|
| EMP_ID | VARCHAR(10) (PK) | Employee ID |
| EMP_NAME | VARCHAR(20) | Employee name |
| SEX | VARCHAR(10) | Gender |
| AGE | INT(5) | Age |
| DESIG | VARCHAR(20) | Designation |
| SAL | INT(10) | Salary |
| EXP | VARCHAR(100) | Experience |
| EMAIL | VARCHAR(20) | Email |
| PHONE | INT(12) | Phone number |

#### **TREATMENT**
| Column | Type | Description |
|--------|------|-------------|
| PATIENT_ID | INT (PK, FK) | References PATIENT |
| TREATMENT | VARCHAR(100) | Treatment description |
| TREATMENT_CODE | VARCHAR(30) | Treatment code |
| T_COST | INT(20) | Treatment cost |

---

## 🧪 Testing the System

### **Run Tests**:
```bash
python test_ai.py
```

### **View Database**:
Use [DB Browser for SQLite](https://sqlitebrowser.org/) to open `HospitalDB.db` and inspect tables.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Developed with ❤️ for Healthcare Management**

- 🏥 Streamlining hospital operations
- 💻 Full-stack Python application
- 🌐 Cross-platform compatibility
- 🤖 AI-ready architecture

---

## 📞 Support

For issues, questions, or contributions:
- Open an [Issue](https://github.com/YOUR_USERNAME/Hospital-Management-System/issues)
- Star ⭐ the repository if you found it helpful!

---

**Made with Python 🐍 | Flask 🌶️ | SQLite 🗄️ | Tkinter 🖥️**
