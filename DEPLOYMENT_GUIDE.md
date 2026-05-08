# 🏥 Hospital Management System - Deployment Guide

## 🎯 Overview
A comprehensive hospital management system with separate Admin and Nurse portals, featuring real-time patient management, medicine inventory, emergency protocols, and AI-powered medical assistance.

## ✨ Features

### Admin Portal
- Patient Management (Admission, Discharge, Transfer)
- Employee Management
- Room & Ward Allocation
- Appointment Scheduling
- Treatment Records
- Medicine Inventory
- Billing System
- AI Medical Assistant
- Complete Database Management

### Nurse Portal
- 👥 Patient Management
- 💊 Medicine Management
- 📅 Doctor Schedule
- 🤖 AI Medical Assistant
- 📋 Nurse Notice Board
- 🏥 Ward Management
- 🩸 Blood Bank Services
- �� Emergency Protocols

## 🚀 Quick Start

### For Mac Users:
1. Double-click `Hospital_System.command`
2. The system will automatically open in your browser
3. Login with credentials provided below

### For Windows Users:
1. Double-click `Hospital_System.bat`
2. The system will automatically open in your browser
3. Login with credentials provided below

### Manual Start (Any Platform):
```bash
python3 app.py
```
Then open: http://127.0.0.1:5002

## 🔐 Login Credentials

### Main Login Page
**Admin Access:**
- Username: `admin`
- Password: `admin123`

**Nurse Access:**
- Click "Go to Nurse Login" button
- Use Nurse ID and password from database

### Nurse Portal Credentials
| Nurse ID | Name | Password |
|----------|------|----------|
| NUR001 | Sarah Johnson | sarah2024 |
| NUR002 | Michael Chen | michael2024 |
| NUR003 | Emily Davis | emily2024 |

## 🌐 Web Deployment

### Running on Local Network:
The system runs on port 5002 by default. To access from other devices on your network:

1. Find your computer's IP address:
   - Mac: `ifconfig | grep inet`
   - Windows: `ipconfig`

2. Access from other devices:
   ```
   http://YOUR_IP_ADDRESS:5002
   ```

### Production Deployment:
For production deployment with better security and performance:

1. Install Gunicorn (production server):
   ```bash
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5002 app:app
   ```

3. Configure firewall to allow port 5002

## 📱 Mobile Access
The system is fully responsive and can be accessed from:
- Smartphones (iOS/Android)
- Tablets (iPad/Android tablets)
- Any device with a web browser

## 🔧 Troubleshooting

### Port Already in Use:
If port 5002 is busy, modify `app.py`:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
```
Change port number to 5003, 8080, etc.

### Browser Not Opening:
Manually navigate to: http://127.0.0.1:5002

### Database Issues:
Run database setup:
```bash
python3 setup_database.py
```

## 📊 Database
The system uses SQLite database (`HospitalDB.db`) with the following tables:
- PATIENT
- EMPLOYEE
- NURSE
- ROOM
- APPOINTMENT
- TREATMENT
- MEDICINE
- CONTACT_NO
- BILLING

## 🛡️ Security Notes
- Change default passwords after deployment
- Use HTTPS in production environments
- Implement proper user authentication
- Regular database backups
- Firewall configuration required for external access

## 📞 Support
For technical support or customization requests, please contact your system administrator.

---
**Version:** 2.0  
**Last Updated:** March 2026  
**Platform:** Cross-Platform (Mac, Windows, Linux)
