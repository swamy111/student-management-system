from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import subprocess
import sys
import threading
import time
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('HospitalDB.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/menu')
def main_menu():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * {

                margin: 0;
                padding: 0;
                box-sizing: border-box;

            }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                position: relative;
                overflow-x: hidden;
            }
            body::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="30" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></svg>');
                background-size: 150px 150px;
                animation: float 20s linear infinite;
            }
            @keyframes float {
                0% { transform: translateY(0); }
                100% { transform: translateY(150px); }
            }
            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                position: relative;
                z-index: 10;
            }
            .header-content {
                max-width: 1400px;
                margin: 0 auto;
                padding: 30px 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .logo-section {
                display: flex;
                align-items: center;
                gap: 20px;
            }
            .hospital-logo {
                width: 80px;
                height: 80px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 40px;
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
                animation: pulse-logo 2s ease-in-out infinite;
            }
            @keyframes pulse-logo {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            .welcome-text h1 {
                color: #2c3e50;
                font-size: 32px;
                font-weight: 700;
                margin-bottom: 5px;
            }
            .welcome-text p {
                color: #7f8c8d;
                font-size: 14px;
            }
            .status-badge {
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                color: white;
                padding: 8px 20px;
                border-radius: 25px;
                font-size: 13px;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 4px 15px rgba(56, 239, 125, 0.3);
            }
            .main-container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 40px 20px;
                position: relative;
                z-index: 5;
            }
            .dashboard-title {
                text-align: center;
                color: white;
                margin-bottom: 40px;
            }
            .dashboard-title h2 {
                font-size: 36px;
                font-weight: 700;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);

            }
            .dashboard-title p {
                font-size: 16px;
                opacity: 0.9;
            }

            .cards-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 25px;
                margin-bottom: 30px;

            }
            .card {
                background: white;
                border-radius: 20px;
                padding: 30px;
                text-decoration: none;
                transition: all 0.3s ease;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                position: relative;
                overflow: hidden;
                display: block;
            }

            .card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                transform: scaleX(0);
                transition: transform 0.3s ease;

            }
            .card:hover::before {
                transform: scaleX(1);
            }

            .card:hover {
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            }
            .card-icon {
                width: 70px;
                height: 70px;
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 32px;
                margin-bottom: 20px;
                transition: all 0.3s ease;
            }
            .card:hover .card-icon {
                transform: scale(1.1) rotate(5deg);
            }
            .card.patient-reg .card-icon {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .card.room-allot .card-icon {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
            }
            .card.employee-reg .card-icon {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
            }
            .card.appointment .card-icon {
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                color: white;
            }
            .card.billing .card-icon {
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                color: white;
            }
            .card.view-patients .card-icon {
                background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
                color: white;
            }
            .card.view-employees .card-icon {
                background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                color: #333;
            }
            .card.view-appointments .card-icon {
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                color: white;
            }
            .card.view-rooms .card-icon {
                background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                color: #333;
            }
            .card-title {
                color: #2c3e50;
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 8px;
            }
            .card-description {
                color: #7f8c8d;
                font-size: 13px;
                line-height: 1.6;
            }
            .card-arrow {
                position: absolute;
                bottom: 20px;
                right: 20px;
                font-size: 20px;
                color: #667eea;
                opacity: 0;
                transform: translateX(-10px);
                transition: all 0.3s ease;
            }
            .card:hover .card-arrow {
                opacity: 1;
                transform: translateX(0);
            }
            .exit-section {
                text-align: center;
                margin-top: 40px;
                padding: 30px;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            
            .exit-btn {
                background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
                color: white;
                padding: 15px 50px;
                border-radius: 30px;
                text-decoration: none;
                font-size: 16px;
                font-weight: 600;
                display: inline-flex;
                align-items: center;
                gap: 10px;
                transition: all 0.3s ease;
                box-shadow: 0 8px 20px rgba(235, 51, 73, 0.3);
            }

            .exit-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 30px rgba(235, 51, 73, 0.4);
            }
            .stats-bar {
                display: flex;
                justify-content: center;
                gap: 30px;
                margin-bottom: 40px;
                flex-wrap: wrap;
            }
            .stat-item {
                background: rgba(255, 255, 255, 0.95);
                padding: 20px 30px;
                border-radius: 15px;
                text-align: center;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 20px rgba(0,0,0,0.1);
                min-width: 150px;
            }
            .stat-number {
                font-size: 32px;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 5px;
            }
            .stat-label {
                color: #7f8c8d;
                font-size: 13px;
                font-weight: 500;
            }
            @media (max-width: 768px) {
                .header-content {
                    flex-direction: column;
                    gap: 20px;
                    text-align: center;
                }
                .logo-section {
                    flex-direction: column;
                }
                .dashboard-title h2 {
                    font-size: 28px;
                }
                .cards-grid {
                    grid-template-columns: 1fr;
                }
                .stats-bar {
                    flex-direction: column;
                    align-items: center;
                }
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">🏥</div>
                    <div class="welcome-text">
                        <h1>Hospital Management System</h1>
                        <p>Comprehensive Healthcare Solutions</p>
                    </div>
                </div>
                <div class="status-badge">
                    <i class="fas fa-check-circle"></i>
                    <span>Database Connected</span>
                </div>
            </div>
        </header>

        <div class="main-container">
            <div class="dashboard-title">
                <h2>👋 Welcome to Your Dashboard</h2>
                <p>Select an option below to get started</p>
            </div>

            <div class="stats-bar">
                <div class="stat-item">
                    <div class="stat-number">24/7</div>
                    <div class="stat-label">Healthcare Support</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">100+</div>
                    <div class="stat-label">Services Available</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">50+</div>
                    <div class="stat-label">Expert Staff</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">500+</div>
                    <div class="stat-label">Happy Patients</div>
                </div>
            </div>

            <div class="cards-grid">
                <a href="/patient" class="card patient-reg">
                    <div class="card-icon">
                        <i class="fas fa-user-plus"></i>
                    </div>
                    <h3 class="card-title">Patient Registration</h3>
                    <p class="card-description">Register new patients with complete medical history and personal information</p>
                    <i class="fas fa-arrow-right card-arrow"></i>
                </a>

                <a href="/room" class="card room-allot">
                    <div class="card-icon">
                        <i class="fas fa-bed"></i>
                    </div>
                    <h3 class="card-title">Room Allocation</h3>
                    <p class="card-description">Assign rooms to patients based on availability and requirements</p>
                    <i class="fas fa-arrow-right card-arrow"></i>
                </a>

                <a href="/employee" class="card employee-reg">
                    <div class="card-icon">
                        <i class="fas fa-user-md"></i>
                    </div>
                    <h3 class="card-title">Employee Registration</h3>
                    <p class="card-description">Add new doctors, nurses, and administrative staff to the system</p>
                    <i class="fas fa-arrow-right card-arrow"></i>
                </a>

                <a href="/appointment" class="card appointment">
                    <div class="card-icon">
                        <i class="fas fa-calendar-check"></i>
                    </div>
                    <h3 class="card-title">Book Appointment</h3>
                    <p class="card-description">Schedule appointments with specialized doctors for patients</p>
                    <i class="fas fa-arrow-right card-arrow"></i>
                </a>

                <a href="/billing" class="card billing">
                    <div class="card-icon">
                        <i class="fas fa-file-invoice-dollar"></i>
                    </div>
                    <h3 class="card-title">Patient Billing</h3>
                    <p class="card-description">Generate and manage patient bills and payment records</p>
                    <i class="fas fa-arrow-right card-arrow"></i>
                </a>

                <a href="/ai-assistant" class="card ai-assistant" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
                    <div class="card-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h3 class="card-title">🤖 AI Medical Assistant</h3>
                    <p class="card-description">Get instant medical information, precautions, and medicine suggestions</p>
                    <i class="fas fa-arrow-right card-arrow"></i>
                </a>

                <a href="/nurse" class="card nurse-management" style="background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);">
                    <div class="card-icon">
                        <i class="fas fa-user-nurse"></i>
                    </div>
                    <h3 class="card-title">💉 Nurse Management</h3>
                    <p class="card-description">Manage nursing staff, shifts, departments, and assignments</p>
                    <i class="fas fa-arrow-right card-arrow"></i>
                </a>

                <a href="/view-nurses" class="card view-nurses" style="background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);">
                    <div class="card-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <h3 class="card-title">📋 View Nurses</h3>
                    <p class="card-description">View complete list of all nurses and their details</p>
                    <i class="fas fa-arrow-right card-arrow"></i>
                </a>

                <a href="/patients" class="card view-patients">
                    <div class="card-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <h3 class="card-title">View Patients</h3>
                    <p class="card-description">Browse and manage all patient records and information</p>
                    <i class="fas fa-arrow-right card-arrow"></i>
                </a>

                <a href="/employees" class="card view-employees">
                    <div class="card-icon">
                        <i class="fas fa-chalkboard-teacher"></i>
                    </div>
                    <h3 class="card-title">View Employees</h3>
                    <p class="card-description">View complete list of hospital staff and their details</p>
                    <i class="fas fa-arrow-right card-arrow"></i>
                </a>

                <a href="/appointments" class="card view-appointments">
                    <div class="card-icon">
                        <i class="fas fa-calendar-alt"></i>
                    </div>
                    <h3 class="card-title">View Appointments</h3>
                    <p class="card-description">Check all scheduled appointments and their status</p>
                    <i class="fas fa-arrow-right card-arrow"></i>
                </a>

                <a href="/rooms" class="card view-rooms">
                    <div class="card-icon">
                        <i class="fas fa-building"></i>
                    </div>
                    <h3 class="card-title">View Rooms</h3>
                    <p class="card-description">Monitor room occupancy and availability across all wards</p>
                    <i class="fas fa-arrow-right card-arrow"></i>
                </a>
            </div>

            <div class="exit-section">
                <a href="/exit" class="exit-btn">
                    <i class="fas fa-sign-out-alt"></i>
                    Exit System
                </a>
            </div>
        </div>
    </body>
    </html>
    '''

# Patient Registration Form Submission
@app.route('/patient/submit', methods=['POST'])
def patient_submit():
    try:
        pat_id = request.form['pat_id']
        pat_name = request.form['pat_name']
        pat_sex = request.form['pat_sex']
        pat_bg = request.form['pat_bg']
        pat_dob = request.form['pat_dob']
        pat_contact = request.form['pat_contact']
        pat_contactalt = request.form.get('pat_contactalt', 0) or 0  # Handle empty value
        pat_address = request.form['pat_address']
        pat_ct = request.form['pat_ct']
        pat_email = request.form['pat_email']
        
        conn = get_db_connection()
        
        # Check if patient already exists
        existing_patient = conn.execute('SELECT * FROM PATIENT WHERE PATIENT_ID = ?', (pat_id,)).fetchone()
        if existing_patient:
            conn.close()
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Error - Patient Registration</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
                    .error { color: #e74c3c; font-size: 18px; }
                    .btn { 
                        background-color: #3498db; 
                        color: white; 
                        padding: 12px 30px; 
                        text-decoration: none; 
                        border-radius: 5px; 
                        display: inline-block; 
                        margin: 10px 5px; 
                    }
                    .btn:hover { background-color: #2980b9; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2 class="error">Error: Patient ID Already Exists</h2>
                    <p>Please use a different Patient ID.</p>
                    <a href="/patient" class="btn">Back to Patient Registration</a>
                    <a href="/" class="btn">Main Menu</a>
                </div>
            </body>
            </html>
            '''
        
        # Insert patient data into PATIENT table
        conn.execute('''INSERT INTO PATIENT (PATIENT_ID, NAME, SEX, BLOOD_GROUP, DOB, ADDRESS, CONSULT_TEAM, EMAIL) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (pat_id, pat_name, pat_sex, pat_bg, pat_dob, pat_address, pat_ct, pat_email))
        
        # Insert contact information into CONTACT_NO table
        conn.execute('''INSERT INTO CONTACT_NO (PATIENT_ID, CONTACTNO, ALT_CONTACT) 
                      VALUES (?, ?, ?)''', 
                      (pat_id, pat_contact, pat_contactalt))
        
        conn.commit()
        conn.close()
        
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Success - Patient Registration</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
                .success { color: #27ae60; font-size: 18px; }
                .btn { 
                    background-color: #3498db; 
                    color: white; 
                    padding: 12px 30px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    display: inline-block; 
                    margin: 10px 5px; 
                }
                .btn:hover { background-color: #2980b9; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="success">Success: Patient Registered</h2>
                <p>Patient details have been successfully saved to the database.</p>
                <a href="/patient" class="btn">Register Another Patient</a>
                <a href="/" class="btn">Main Menu</a>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f'''<!DOCTYPE html>
        <html>
        <head>
            <title>Error - Patient Registration</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }}
                .error {{ color: #e74c3c; font-size: 18px; }}
                .btn {{ 
                    background-color: #3498db; 
                    color: white; 
                    padding: 12px 30px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    display: inline-block; 
                    margin: 10px 5px; 
                }}
                .btn:hover {{ background-color: #2980b9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="error">Error: {str(e)}</h2>
                <a href="/patient" class="btn">Back to Patient Registration</a>
                <a href="/" class="btn">Main Menu</a>
            </div>
        </body>
        </html>
        '''

@app.route('/patient')
def patient():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Patient Registration - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                position: relative;
                overflow-x: hidden;
            }
            body::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="2"/></svg>');
                background-size: 120px 120px;
                animation: float 15s linear infinite;
            }
            @keyframes float {
                0% { transform: translateY(0); }
                100% { transform: translateY(-120px); }
            }
            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                padding: 20px 0;
                position: relative;
                z-index: 10;
            }
            .header-content {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .logo-section {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .hospital-logo {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 30px;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            .page-title h1 {
                color: #2c3e50;
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 5px;
            }
            .page-title p {
                color: #7f8c8d;
                font-size: 14px;
            }
            .main-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
                position: relative;
                z-index: 5;
            }
            .form-card {
                background: white;
                border-radius: 20px;
                padding: 50px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                position: relative;
                overflow: hidden;
            }
            .form-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 6px;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            }
            .section-header {
                text-align: center;
                margin-bottom: 40px;
            }
            .section-icon {
                width: 80px;
                height: 80px;
                margin: 0 auto 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 36px;
                color: white;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
                animation: pulse-icon 2s ease-in-out infinite;
            }
            @keyframes pulse-icon {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            .section-header h2 {
                color: #2c3e50;
                font-size: 32px;
                font-weight: 700;
                margin-bottom: 10px;
            }
            .section-header p {
                color: #7f8c8d;
                font-size: 15px;
            }
            .form-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 25px;
                margin-bottom: 30px;
            }
            .form-group {
                position: relative;
            }
            .form-group label {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 10px;
                font-weight: 600;
                color: #2c3e50;
                font-size: 14px;
            }
            .form-group label i {
                color: #667eea;
                font-size: 16px;
            }
            .form-group input,
            .form-group textarea,
            .form-group select {
                width: 100%;
                padding: 14px 18px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 14px;
                font-family: 'Poppins', sans-serif;
                transition: all 0.3s ease;
                background: white;
            }
            .form-group input:focus,
            .form-group textarea:focus,
            .form-group select:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
            }
            .form-group textarea {
                resize: vertical;
                min-height: 100px;
            }
            .full-width {
                grid-column: 1 / -1;
            }
            .form-actions {
                display: flex;
                gap: 15px;
                justify-content: center;
                margin-top: 40px;
                padding-top: 30px;
                border-top: 2px solid #f0f0f0;
            }
            .btn {
                padding: 14px 40px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 10px;
                transition: all 0.3s ease;
                cursor: pointer;
                border: none;
                font-family: 'Poppins', sans-serif;
            }
            .submit-btn {
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                color: white;
                box-shadow: 0 8px 20px rgba(67, 233, 123, 0.3);
            }
            .submit-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 30px rgba(67, 233, 123, 0.4);
            }
            .back-btn {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #2c3e50;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .back-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            }
            .info-badge {
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                border-left: 4px solid #2196f3;
                padding: 15px 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .info-badge i {
                font-size: 24px;
                color: #2196f3;
            }
            .info-badge p {
                color: #1976d2;
                font-size: 14px;
                margin: 0;
            }
            @media (max-width: 768px) {
                .form-card {
                    padding: 30px 20px;
                }
                .form-grid {
                    grid-template-columns: 1fr;
                }
                .form-actions {
                    flex-direction: column;
                }
                .btn {
                    width: 100%;
                    justify-content: center;
                }
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">🏥</div>
                    <div class="page-title">
                        <h1>Patient Registration</h1>
                        <p>Register new patients to the system</p>
                    </div>
                </div>
            </div>
        </header>

        <div class="main-container">
            <div class="form-card">
                <div class="section-header">
                    <div class="section-icon">
                        <i class="fas fa-user-plus"></i>
                    </div>
                    <h2>Patient Information Form</h2>
                    <p>Please fill in all required fields to register a new patient</p>
                </div>

                <div class="info-badge">
                    <i class="fas fa-info-circle"></i>
                    <p><strong>Note:</strong> All fields marked with * are mandatory. Please ensure all information is accurate before submission.</p>
                </div>

                <form action="/patient/submit" method="POST">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="pat_id">
                                <i class="fas fa-id-card"></i>
                                Patient ID *
                            </label>
                            <input type="number" id="pat_id" name="pat_id" placeholder="Enter unique patient ID" required>
                        </div>

                        <div class="form-group">
                            <label for="pat_name">
                                <i class="fas fa-user"></i>
                                Patient Name *
                            </label>
                            <input type="text" id="pat_name" name="pat_name" placeholder="Full name of the patient" required>
                        </div>

                        <div class="form-group">
                            <label for="pat_sex">
                                <i class="fas fa-venus-mars"></i>
                                Sex *
                            </label>
                            <select id="pat_sex" name="pat_sex" required>
                                <option value="">Select gender</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="pat_bg">
                                <i class="fas fa-tint"></i>
                                Blood Group *
                            </label>
                            <select id="pat_bg" name="pat_bg" required>
                                <option value="">Select blood group</option>
                                <option value="A+">A+</option>
                                <option value="A-">A-</option>
                                <option value="B+">B+</option>
                                <option value="B-">B-</option>
                                <option value="AB+">AB+</option>
                                <option value="AB-">AB-</option>
                                <option value="O+">O+</option>
                                <option value="O-">O-</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="pat_dob">
                                <i class="fas fa-calendar-alt"></i>
                                Date of Birth *
                            </label>
                            <input type="date" id="pat_dob" name="pat_dob" required>
                        </div>

                        <div class="form-group">
                            <label for="pat_contact">
                                <i class="fas fa-phone"></i>
                                Primary Contact *
                            </label>
                            <input type="number" id="pat_contact" name="pat_contact" placeholder="Primary phone number" required>
                        </div>

                        <div class="form-group">
                            <label for="pat_contactalt">
                                <i class="fas fa-phone-alt"></i>
                                Alternate Contact
                            </label>
                            <input type="number" id="pat_contactalt" name="pat_contactalt" placeholder="Secondary phone number">
                        </div>

                        <div class="form-group">
                            <label for="pat_email">
                                <i class="fas fa-envelope"></i>
                                Email Address *
                            </label>
                            <input type="email" id="pat_email" name="pat_email" placeholder="patient@example.com" required>
                        </div>

                        <div class="form-group">
                            <label for="pat_ct">
                                <i class="fas fa-user-md"></i>
                                Consulting Doctor/Team *
                            </label>
                            <input type="text" id="pat_ct" name="pat_ct" placeholder="Dr. Name or Department" required>
                        </div>

                        <div class="form-group full-width">
                            <label for="pat_address">
                                <i class="fas fa-map-marker-alt"></i>
                                Complete Address *
                            </label>
                            <textarea id="pat_address" name="pat_address" placeholder="Enter complete postal address with street, city, state, and ZIP code" required></textarea>
                        </div>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn submit-btn">
                            <i class="fas fa-check-circle"></i>
                            Register Patient
                        </button>
                        <a href="/" class="btn back-btn">
                            <i class="fas fa-arrow-left"></i>
                            Back to Dashboard
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    '''
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Patient Registration</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .form-group { margin: 15px 0; }
            .form-row { display: flex; flex-wrap: wrap; }
            .form-col { flex: 1; min-width: 200px; padding: 10px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; color: #2c3e50; }
            input[type=text], input[type=email], input[type=date], input[type=number] {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            .btn {
                background-color: #3498db;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 5px;
                display: inline-block;
                margin: 10px 5px;
                cursor: pointer;
            }
            .btn:hover { background-color: #2980b9; }
            .back-btn { background-color: #95a5a6; }
            .back-btn:hover { background-color: #7f8c8d; }
            .submit-btn { background-color: #2ecc71; }
            .submit-btn:hover { background-color: #27ae60; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>PATIENT REGISTRATION FORM</h1>
            <form action="/patient/submit" method="POST">
                <div class="form-row">
                    <div class="form-col">
                        <div class="form-group">
                            <label for="pat_id">Patient ID:</label>
                            <input type="number" id="pat_id" name="pat_id" required>
                        </div>
                        <div class="form-group">
                            <label for="pat_name">Patient Name:</label>
                            <input type="text" id="pat_name" name="pat_name" required>
                        </div>
                        <div class="form-group">
                            <label for="pat_sex">Sex:</label>
                            <input type="text" id="pat_sex" name="pat_sex" required>
                        </div>
                        <div class="form-group">
                            <label for="pat_bg">Blood Group:</label>
                            <input type="text" id="pat_bg" name="pat_bg" required>
                        </div>
                    </div>
                    <div class="form-col">
                        <div class="form-group">
                            <label for="pat_dob">Date of Birth (YYYY-MM-DD):</label>
                            <input type="date" id="pat_dob" name="pat_dob" required>
                        </div>
                        <div class="form-group">
                            <label for="pat_contact">Contact Number:</label>
                            <input type="number" id="pat_contact" name="pat_contact" required>
                        </div>
                        <div class="form-group">
                            <label for="pat_contactalt">Alternate Contact:</label>
                            <input type="number" id="pat_contactalt" name="pat_contactalt">
                        </div>
                        <div class="form-group">
                            <label for="pat_email">Email:</label>
                            <input type="email" id="pat_email" name="pat_email" required>
                        </div>
                    </div>
                    <div class="form-col">
                        <div class="form-group">
                            <label for="pat_ct">Consulting Team / Doctor:</label>
                            <input type="text" id="pat_ct" name="pat_ct" required>
                        </div>
                        <div class="form-group">
                            <label for="pat_address">Address:</label>
                            <textarea id="pat_address" name="pat_address" rows="4" cols="30" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;" required></textarea>
                        </div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 20px;">
                    <input type="submit" value="Submit" class="btn submit-btn">
                    <a href="/" class="btn back-btn">Back to Main Menu</a>
                </div>
            </form>
        </div>
    </body>
    </html>
    '''

# Room Allocation Form
@app.route('/room')
def room():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Room Allocation - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                position: relative;
                overflow-x: hidden;
            }
            body::before {
                content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="25" y="25" width="50" height="50" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="2"/></svg>');
                background-size: 100px 100px; animation: float 15s linear infinite;
            }
            @keyframes float { 0% { transform: translateY(0); } 100% { transform: translateY(-100px); } }
            .header {
                background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1); padding: 20px 0; position: relative; z-index: 10;
            }
            .header-content {
                max-width: 1200px; margin: 0 auto; padding: 0 20px;
                display: flex; align-items: center; justify-content: space-between;
            }
            .logo-section { display: flex; align-items: center; gap: 15px; }
            .hospital-logo {
                width: 60px; height: 60px;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 15px; display: flex; align-items: center; justify-content: center;
                font-size: 30px; box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
            }
            .page-title h1 { color: #2c3e50; font-size: 28px; font-weight: 700; margin-bottom: 5px; }
            .page-title p { color: #7f8c8d; font-size: 14px; }
            .main-container {
                max-width: 1200px; margin: 0 auto; padding: 40px 20px; position: relative; z-index: 5;
            }
            .form-card {
                background: white; border-radius: 20px; padding: 50px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2); position: relative; overflow: hidden;
            }
            .form-card::before {
                content: ''; position: absolute; top: 0; left: 0; right: 0; height: 6px;
                background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
            }
            .section-header { text-align: center; margin-bottom: 40px; }
            .section-icon {
                width: 80px; height: 80px; margin: 0 auto 20px;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 20px; display: flex; align-items: center; justify-content: center;
                font-size: 36px; color: white; box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
                animation: pulse-icon 2s ease-in-out infinite;
            }
            @keyframes pulse-icon { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
            .section-header h2 { color: #2c3e50; font-size: 32px; font-weight: 700; margin-bottom: 10px; }
            .section-header p { color: #7f8c8d; font-size: 15px; }
            .rate-cards {
                display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px; margin-bottom: 30px;
            }
            .rate-card {
                background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                padding: 20px; border-radius: 15px; text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.1); transition: all 0.3s ease;
            }
            .rate-card:hover { transform: translateY(-5px); box-shadow: 0 12px 30px rgba(0,0,0,0.15); }
            .rate-card i { font-size: 32px; color: #f5576c; margin-bottom: 10px; }
            .rate-card h3 { color: #2c3e50; font-size: 16px; margin-bottom: 5px; }
            .rate-card .price { color: #f5576c; font-size: 24px; font-weight: 700; }
            .form-grid {
                display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 25px; margin-bottom: 30px;
            }
            .form-group { position: relative; }
            .form-group label {
                display: flex; align-items: center; gap: 8px;
                margin-bottom: 10px; font-weight: 600; color: #2c3e50; font-size: 14px;
            }
            .form-group label i { color: #f093fb; font-size: 16px; }
            .form-group input, .form-group select {
                width: 100%; padding: 14px 18px; border: 2px solid #e0e0e0;
                border-radius: 10px; font-size: 14px; font-family: 'Poppins', sans-serif;
                transition: all 0.3s ease;
            }
            .form-group input:focus, .form-group select:focus {
                outline: none; border-color: #f093fb;
                box-shadow: 0 0 0 4px rgba(240, 147, 251, 0.1);
            }
            .form-actions {
                display: flex; gap: 15px; justify-content: center;
                margin-top: 40px; padding-top: 30px; border-top: 2px solid #f0f0f0;
            }
            .btn {
                padding: 14px 40px; border-radius: 10px; font-size: 16px; font-weight: 600;
                text-decoration: none; display: inline-flex; align-items: center; gap: 10px;
                transition: all 0.3s ease; cursor: pointer; border: none; font-family: 'Poppins', sans-serif;
            }
            .submit-btn {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white; box-shadow: 0 8px 20px rgba(240, 147, 251, 0.3);
            }
            .submit-btn:hover { transform: translateY(-3px); box-shadow: 0 12px 30px rgba(240, 147, 251, 0.4); }
            .back-btn {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #2c3e50; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .back-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
            @media (max-width: 768px) {
                .form-card { padding: 30px 20px; }
                .form-grid { grid-template-columns: 1fr; }
                .form-actions { flex-direction: column; }
                .btn { width: 100%; justify-content: center; }
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">🏥</div>
                    <div class="page-title">
                        <h1>Room Allocation</h1>
                        <p>Assign rooms to patients efficiently</p>
                    </div>
                </div>
            </div>
        </header>
        <div class="main-container">
            <div class="form-card">
                <div class="section-header">
                    <div class="section-icon"><i class="fas fa-bed"></i></div>
                    <h2>Allocate Hospital Room</h2>
                    <p>Select appropriate room type and enter patient details</p>
                </div>
                <div class="rate-cards">
                    <div class="rate-card">
                        <i class="fas fa-user"></i>
                        <h3>Single Room</h3>
                        <div class="price">₹4500/day</div>
                    </div>
                    <div class="rate-card">
                        <i class="fas fa-users"></i>
                        <h3>Twin Sharing</h3>
                        <div class="price">₹2500/day</div>
                    </div>
                    <div class="rate-card">
                        <i class="fas fa-users"></i>
                        <h3>Triple Sharing</h3>
                        <div class="price">₹2000/day</div>
                    </div>
                </div>
                <form action="/room/submit" method="POST">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="pat_id"><i class="fas fa-id-card"></i> Patient ID *</label>
                            <input type="number" id="pat_id" name="pat_id" placeholder="Enter patient ID" required>
                        </div>
                        <div class="form-group">
                            <label for="room_type"><i class="fas fa-door-open"></i> Room Type *</label>
                            <select id="room_type" name="room_type" required>
                                <option value="">Select room type</option>
                                <option value="SINGLE">Single Room (₹4500)</option>
                                <option value="TWIN">Twin Sharing (₹2500)</option>
                                <option value="TRIPLE">Triple Sharing (₹2000)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="room_no"><i class="fas fa-hashtag"></i> Room Number *</label>
                            <input type="text" id="room_no" name="room_no" placeholder="e.g., 101, 205" required>
                        </div>
                        <div class="form-group">
                            <label for="rate"><i class="fas fa-rupee-sign"></i> Room Charges (₹) *</label>
                            <input type="number" id="rate" name="rate" placeholder="Enter room rate" required>
                        </div>
                        <div class="form-group">
                            <label for="date_admitted"><i class="fas fa-calendar-check"></i> Date Admitted *</label>
                            <input type="date" id="date_admitted" name="date_admitted" required>
                        </div>
                        <div class="form-group">
                            <label for="date_discharged"><i class="fas fa-calendar-times"></i> Date Discharged</label>
                            <input type="date" id="date_discharged" name="date_discharged">
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn submit-btn">
                            <i class="fas fa-check-circle"></i> Allocate Room
                        </button>
                        <a href="/" class="btn back-btn">
                            <i class="fas fa-arrow-left"></i> Back to Dashboard
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/room/submit', methods=['POST'])
def room_submit():
    try:
        pat_id = request.form['pat_id']
        room_type = request.form['room_type']
        room_no = request.form['room_no']
        rate = request.form['rate']
        date_admitted = request.form['date_admitted']
        date_discharged = request.form.get('date_discharged', None)
        
        conn = get_db_connection()
        
        # Check if room is already occupied
        existing_room = conn.execute('SELECT * FROM ROOM WHERE ROOM_NO = ?', (room_no,)).fetchone()
        if existing_room:
            conn.close()
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Error - Room Allocation</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
                    .error { color: #e74c3c; font-size: 18px; }
                    .btn { 
                        background-color: #3498db; 
                        color: white; 
                        padding: 12px 30px; 
                        text-decoration: none; 
                        border-radius: 5px; 
                        display: inline-block; 
                        margin: 10px 5px; 
                    }
                    .btn:hover { background-color: #2980b9; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2 class="error">Error: Room is Currently Occupied</h2>
                    <p>Please select a different room number.</p>
                    <a href="/room" class="btn">Back to Room Allocation</a>
                    <a href="/" class="btn">Main Menu</a>
                </div>
            </body>
            </html>
            '''
        
        # Insert room allocation data
        conn.execute('''INSERT INTO ROOM (PATIENT_ID, ROOM_NO, ROOM_TYPE, RATE, DATE_ADMITTED, DATE_DISCHARGED) 
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                      (pat_id, room_no, room_type, rate, date_admitted, date_discharged))
        
        conn.commit()
        conn.close()
        
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Success - Room Allocation</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
                .success { color: #27ae60; font-size: 18px; }
                .btn { 
                    background-color: #3498db; 
                    color: white; 
                    padding: 12px 30px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    display: inline-block; 
                    margin: 10px 5px; 
                }
                .btn:hover { background-color: #2980b9; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="success">Success: Room Allocated</h2>
                <p>Room has been successfully allocated to the patient.</p>
                <a href="/room" class="btn">Allocate Another Room</a>
                <a href="/" class="btn">Main Menu</a>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f'''<!DOCTYPE html>
        <html>
        <head>
            <title>Error - Room Allocation</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }}
                .error {{ color: #e74c3c; font-size: 18px; }}
                .btn {{ 
                    background-color: #3498db; 
                    color: white; 
                    padding: 12px 30px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    display: inline-block; 
                    margin: 10px 5px; 
                }}
                .btn:hover {{ background-color: #2980b9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="error">Error: {str(e)}</h2>
                <a href="/room" class="btn">Back to Room Allocation</a>
                <a href="/" class="btn">Main Menu</a>
            </div>
        </body>
        </html>
        '''

# Employee Registration Form
@app.route('/employee')
def employee():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Employee Registration - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                position: relative; overflow-x: hidden;
            }
            body::before {
                content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><polygon points="50,10 90,90 10,90" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="2"/></svg>');
                background-size: 100px 100px; animation: float 15s linear infinite;
            }
            @keyframes float { 0% { transform: translateY(0); } 100% { transform: translateY(-100px); } }
            .header {
                background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1); padding: 20px 0; position: relative; z-index: 10;
            }
            .header-content {
                max-width: 1200px; margin: 0 auto; padding: 0 20px;
                display: flex; align-items: center; justify-content: space-between;
            }
            .logo-section { display: flex; align-items: center; gap: 15px; }
            .hospital-logo {
                width: 60px; height: 60px;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                border-radius: 15px; display: flex; align-items: center; justify-content: center;
                font-size: 30px; box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
            }
            .page-title h1 { color: #2c3e50; font-size: 28px; font-weight: 700; margin-bottom: 5px; }
            .page-title p { color: #7f8c8d; font-size: 14px; }
            .main-container {
                max-width: 1200px; margin: 0 auto; padding: 40px 20px; position: relative; z-index: 5;
            }
            .form-card {
                background: white; border-radius: 20px; padding: 50px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2); position: relative; overflow: hidden;
            }
            .form-card::before {
                content: ''; position: absolute; top: 0; left: 0; right: 0; height: 6px;
                background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            }
            .section-header { text-align: center; margin-bottom: 40px; }
            .section-icon {
                width: 80px; height: 80px; margin: 0 auto 20px;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                border-radius: 20px; display: flex; align-items: center; justify-content: center;
                font-size: 36px; color: white; box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
                animation: pulse-icon 2s ease-in-out infinite;
            }
            @keyframes pulse-icon { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
            .section-header h2 { color: #2c3e50; font-size: 32px; font-weight: 700; margin-bottom: 10px; }
            .section-header p { color: #7f8c8d; font-size: 15px; }
            .form-grid {
                display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 25px; margin-bottom: 30px;
            }
            .form-group { position: relative; }
            .form-group label {
                display: flex; align-items: center; gap: 8px;
                margin-bottom: 10px; font-weight: 600; color: #2c3e50; font-size: 14px;
            }
            .form-group label i { color: #4facfe; font-size: 16px; }
            .form-group input, .form-group select {
                width: 100%; padding: 14px 18px; border: 2px solid #e0e0e0;
                border-radius: 10px; font-size: 14px; font-family: 'Poppins', sans-serif;
                transition: all 0.3s ease;
            }
            .form-group input:focus, .form-group select:focus {
                outline: none; border-color: #4facfe;
                box-shadow: 0 0 0 4px rgba(79, 172, 254, 0.1);
            }
            .form-actions {
                display: flex; gap: 15px; justify-content: center;
                margin-top: 40px; padding-top: 30px; border-top: 2px solid #f0f0f0;
            }
            .btn {
                padding: 14px 40px; border-radius: 10px; font-size: 16px; font-weight: 600;
                text-decoration: none; display: inline-flex; align-items: center; gap: 10px;
                transition: all 0.3s ease; cursor: pointer; border: none; font-family: 'Poppins', sans-serif;
            }
            .submit-btn {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white; box-shadow: 0 8px 20px rgba(79, 172, 254, 0.3);
            }
            .submit-btn:hover { transform: translateY(-3px); box-shadow: 0 12px 30px rgba(79, 172, 254, 0.4); }
            .back-btn {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #2c3e50; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .back-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
            @media (max-width: 768px) {
                .form-card { padding: 30px 20px; }
                .form-grid { grid-template-columns: 1fr; }
                .form-actions { flex-direction: column; }
                .btn { width: 100%; justify-content: center; }
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">🏥</div>
                    <div class="page-title">
                        <h1>Employee Registration</h1>
                        <p>Add new staff members to the hospital team</p>
                    </div>
                </div>
            </div>
        </header>
        <div class="main-container">
            <div class="form-card">
                <div class="section-header">
                    <div class="section-icon"><i class="fas fa-user-md"></i></div>
                    <h2>Staff Information Form</h2>
                    <p>Register doctors, nurses, and administrative staff</p>
                </div>
                <form action="/employee/submit" method="POST">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="emp_id"><i class="fas fa-id-badge"></i> Employee ID *</label>
                            <input type="text" id="emp_id" name="emp_id" placeholder="Enter unique employee ID" required>
                        </div>
                        <div class="form-group">
                            <label for="emp_name"><i class="fas fa-user"></i> Employee Name *</label>
                            <input type="text" id="emp_name" name="emp_name" placeholder="Full name of employee" required>
                        </div>
                        <div class="form-group">
                            <label for="emp_sex"><i class="fas fa-venus-mars"></i> Gender *</label>
                            <select id="emp_sex" name="emp_sex" required>
                                <option value="">Select gender</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="emp_age"><i class="fas fa-birthday-cake"></i> Age *</label>
                            <input type="number" id="emp_age" name="emp_age" placeholder="Age in years" required>
                        </div>
                        <div class="form-group">
                            <label for="emp_type"><i class="fas fa-briefcase"></i> Designation *</label>
                            <input type="text" id="emp_type" name="emp_type" placeholder="e.g., Doctor, Nurse, Admin" required>
                        </div>
                        <div class="form-group">
                            <label for="emp_salary"><i class="fas fa-rupee-sign"></i> Salary (₹) *</label>
                            <input type="number" id="emp_salary" name="emp_salary" placeholder="Annual salary" required>
                        </div>
                        <div class="form-group">
                            <label for="emp_exp"><i class="fas fa-medal"></i> Experience *</label>
                            <input type="text" id="emp_exp" name="emp_exp" placeholder="e.g., 5 years" required>
                        </div>
                        <div class="form-group">
                            <label for="emp_phone"><i class="fas fa-phone"></i> Contact Number *</label>
                            <input type="number" id="emp_phone" name="emp_phone" placeholder="Primary phone number" required>
                        </div>
                        <div class="form-group full-width">
                            <label for="emp_email"><i class="fas fa-envelope"></i> Email Address *</label>
                            <input type="email" id="emp_email" name="emp_email" placeholder="employee@hospital.com" required>
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn submit-btn">
                            <i class="fas fa-check-circle"></i> Register Employee
                        </button>
                        <a href="/" class="btn back-btn">
                            <i class="fas fa-arrow-left"></i> Back to Dashboard
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/employee/submit', methods=['POST'])
def employee_submit():
    try:
        emp_id = request.form['emp_id']
        emp_name = request.form['emp_name']
        emp_sex = request.form['emp_sex']
        emp_age = request.form['emp_age']
        emp_type = request.form['emp_type']
        emp_salary = request.form['emp_salary']
        emp_exp = request.form['emp_exp']
        emp_email = request.form['emp_email']
        emp_phone = request.form['emp_phone']
        
        conn = get_db_connection()
        
        # Check if employee already exists
        existing_employee = conn.execute('SELECT * FROM EMPLOYEE WHERE EMP_ID = ?', (emp_id,)).fetchone()
        if existing_employee:
            conn.close()
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Error - Employee Registration</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
                    .error { color: #e74c3c; font-size: 18px; }
                    .btn { 
                        background-color: #3498db; 
                        color: white; 
                        padding: 12px 30px; 
                        text-decoration: none; 
                        border-radius: 5px; 
                        display: inline-block; 
                        margin: 10px 5px; 
                    }
                    .btn:hover { background-color: #2980b9; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2 class="error">Error: Employee ID Already Exists</h2>
                    <p>Please use a different Employee ID.</p>
                    <a href="/employee" class="btn">Back to Employee Registration</a>
                    <a href="/" class="btn">Main Menu</a>
                </div>
            </body>
            </html>
            '''
        
        # Insert employee data
        conn.execute('''INSERT INTO EMPLOYEE (EMP_ID, EMP_NAME, SEX, AGE, DESIG, SAL, EXP, EMAIL, PHONE) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (emp_id, emp_name, emp_sex, emp_age, emp_type, emp_salary, emp_exp, emp_email, emp_phone))
        
        conn.commit()
        conn.close()
        
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Success - Employee Registration</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
                .success { color: #27ae60; font-size: 18px; }
                .btn { 
                    background-color: #3498db; 
                    color: white; 
                    padding: 12px 30px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    display: inline-block; 
                    margin: 10px 5px; 
                }
                .btn:hover { background-color: #2980b9; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="success">Success: Employee Registered</h2>
                <p>Employee details have been successfully saved to the database.</p>
                <a href="/employee" class="btn">Register Another Employee</a>
                <a href="/" class="btn">Main Menu</a>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f'''<!DOCTYPE html>
        <html>
        <head>
            <title>Error - Employee Registration</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }}
                .error {{ color: #e74c3c; font-size: 18px; }}
                .btn {{ 
                    background-color: #3498db; 
                    color: white; 
                    padding: 12px 30px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    display: inline-block; 
                    margin: 10px 5px; 
                }}
                .btn:hover {{ background-color: #2980b9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="error">Error: {str(e)}</h2>
                <a href="/employee" class="btn">Back to Employee Registration</a>
                <a href="/" class="btn">Main Menu</a>
            </div>
        </body>
        </html>
        '''

# Appointment Booking Form
@app.route('/appointment')
def appointment():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Book Appointment - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                position: relative; overflow-x: hidden;
            }
            body::before {
                content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="35" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="2"/></svg>');
                background-size: 110px 110px; animation: float 15s linear infinite;
            }
            @keyframes float { 0% { transform: translateY(0); } 100% { transform: translateY(-110px); } }
            .header {
                background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1); padding: 20px 0; position: relative; z-index: 10;
            }
            .header-content {
                max-width: 1200px; margin: 0 auto; padding: 0 20px;
                display: flex; align-items: center; justify-content: space-between;
            }
            .logo-section { display: flex; align-items: center; gap: 15px; }
            .hospital-logo {
                width: 60px; height: 60px;
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                border-radius: 15px; display: flex; align-items: center; justify-content: center;
                font-size: 30px; box-shadow: 0 4px 15px rgba(67, 233, 123, 0.3);
            }
            .page-title h1 { color: #2c3e50; font-size: 28px; font-weight: 700; margin-bottom: 5px; }
            .page-title p { color: #7f8c8d; font-size: 14px; }
            .main-container {
                max-width: 1200px; margin: 0 auto; padding: 40px 20px; position: relative; z-index: 5;
            }
            .form-card {
                background: white; border-radius: 20px; padding: 50px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2); position: relative; overflow: hidden;
            }
            .form-card::before {
                content: ''; position: absolute; top: 0; left: 0; right: 0; height: 6px;
                background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
            }
            .section-header { text-align: center; margin-bottom: 40px; }
            .section-icon {
                width: 80px; height: 80px; margin: 0 auto 20px;
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                border-radius: 20px; display: flex; align-items: center; justify-content: center;
                font-size: 36px; color: white; box-shadow: 0 10px 30px rgba(67, 233, 123, 0.3);
                animation: pulse-icon 2s ease-in-out infinite;
            }
            @keyframes pulse-icon { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
            .section-header h2 { color: #2c3e50; font-size: 32px; font-weight: 700; margin-bottom: 10px; }
            .section-header p { color: #7f8c8d; font-size: 15px; }
            .info-box {
                background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
                border-left: 4px solid #43e97b; padding: 20px; border-radius: 10px;
                margin-bottom: 30px; display: flex; align-items: center; gap: 15px;
            }
            .info-box i { font-size: 28px; color: #2e7d32; }
            .info-box p { color: #1b5e20; font-size: 14px; margin: 0; }
            .form-grid {
                display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 25px; margin-bottom: 30px;
            }
            .form-group { position: relative; }
            .form-group label {
                display: flex; align-items: center; gap: 8px;
                margin-bottom: 10px; font-weight: 600; color: #2c3e50; font-size: 14px;
            }
            .form-group label i { color: #43e97b; font-size: 16px; }
            .form-group input, .form-group textarea {
                width: 100%; padding: 14px 18px; border: 2px solid #e0e0e0;
                border-radius: 10px; font-size: 14px; font-family: 'Poppins', sans-serif;
                transition: all 0.3s ease;
            }
            .form-group input:focus, .form-group textarea:focus {
                outline: none; border-color: #43e97b;
                box-shadow: 0 0 0 4px rgba(67, 233, 123, 0.1);
            }
            .form-group textarea { resize: vertical; min-height: 100px; }
            .form-actions {
                display: flex; gap: 15px; justify-content: center;
                margin-top: 40px; padding-top: 30px; border-top: 2px solid #f0f0f0;
            }
            .btn {
                padding: 14px 40px; border-radius: 10px; font-size: 16px; font-weight: 600;
                text-decoration: none; display: inline-flex; align-items: center; gap: 10px;
                transition: all 0.3s ease; cursor: pointer; border: none; font-family: 'Poppins', sans-serif;
            }
            .submit-btn {
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                color: white; box-shadow: 0 8px 20px rgba(67, 233, 123, 0.3);
            }
            .submit-btn:hover { transform: translateY(-3px); box-shadow: 0 12px 30px rgba(67, 233, 123, 0.4); }
            .back-btn {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #2c3e50; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .back-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
            @media (max-width: 768px) {
                .form-card { padding: 30px 20px; }
                .form-grid { grid-template-columns: 1fr; }
                .form-actions { flex-direction: column; }
                .btn { width: 100%; justify-content: center; }
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">🏥</div>
                    <div class="page-title">
                        <h1>Book Appointment</h1>
                        <p>Schedule consultation with our expert doctors</p>
                    </div>
                </div>
            </div>
        </header>
        <div class="main-container">
            <div class="form-card">
                <div class="section-header">
                    <div class="section-icon"><i class="fas fa-calendar-check"></i></div>
                    <h2>Appointment Booking Form</h2>
                    <p>Fill in the details to schedule your appointment</p>
                </div>
                <div class="info-box">
                    <i class="fas fa-info-circle"></i>
                    <p><strong>Note:</strong> Please ensure all information is accurate. Our receptionist will confirm your appointment via phone call.</p>
                </div>
                <form action="/appointment/submit" method="POST">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="pat_id"><i class="fas fa-user"></i> Patient ID *</label>
                            <input type="number" id="pat_id" name="pat_id" placeholder="Enter patient ID" required>
                        </div>
                        <div class="form-group">
                            <label for="doc_id"><i class="fas fa-user-md"></i> Doctor ID *</label>
                            <input type="text" id="doc_id" name="doc_id" placeholder="Enter doctor ID" required>
                        </div>
                        <div class="form-group">
                            <label for="ap_no"><i class="fas fa-hashtag"></i> Appointment Number *</label>
                            <input type="text" id="ap_no" name="ap_no" placeholder="Auto-generated or enter manually" required>
                        </div>
                        <div class="form-group">
                            <label for="ap_date"><i class="fas fa-calendar-alt"></i> Appointment Date *</label>
                            <input type="date" id="ap_date" name="ap_date" required>
                        </div>
                        <div class="form-group">
                            <label for="ap_time"><i class="fas fa-clock"></i> Appointment Time *</label>
                            <input type="time" id="ap_time" name="ap_time" required>
                        </div>
                        <div class="form-group full-width">
                            <label for="description"><i class="fas fa-comment-medical"></i> Description / Reason *</label>
                            <textarea id="description" name="description" placeholder="Briefly describe the reason for appointment or symptoms" required></textarea>
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn submit-btn">
                            <i class="fas fa-check-circle"></i> Book Appointment
                        </button>
                        <a href="/" class="btn back-btn">
                            <i class="fas fa-arrow-left"></i> Back to Dashboard
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/appointment/submit', methods=['POST'])
def appointment_submit():
    try:
        pat_id = request.form['pat_id']
        doc_id = request.form['doc_id']
        ap_no = request.form['ap_no']
        ap_time = request.form['ap_time']
        ap_date = request.form['ap_date']
        description = request.form['description']
        
        conn = get_db_connection()
        
        # Check if appointment already exists
        existing_appointment = conn.execute('SELECT * FROM APPOINTMENT WHERE AP_NO = ?', (ap_no,)).fetchone()
        if existing_appointment:
            conn.close()
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Error - Appointment Booking</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
                    .error { color: #e74c3c; font-size: 18px; }
                    .btn { 
                        background-color: #3498db; 
                        color: white; 
                        padding: 12px 30px; 
                        text-decoration: none; 
                        border-radius: 5px; 
                        display: inline-block; 
                        margin: 10px 5px; 
                    }
                    .btn:hover { background-color: #2980b9; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2 class="error">Error: Appointment Already Exists</h2>
                    <p>Please use a different Appointment Number.</p>
                    <a href="/appointment" class="btn">Back to Appointment Booking</a>
                    <a href="/" class="btn">Main Menu</a>
                </div>
            </body>
            </html>
            '''
        
        # Insert appointment data
        conn.execute('''INSERT INTO APPOINTMENT (PATIENT_ID, EMP_ID, AP_NO, AP_TIME, AP_DATE, DESCRIPTION) 
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                      (pat_id, doc_id, ap_no, ap_time, ap_date, description))
        
        conn.commit()
        conn.close()
        
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Success - Appointment Booking</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
                .success { color: #27ae60; font-size: 18px; }
                .btn { 
                    background-color: #3498db; 
                    color: white; 
                    padding: 12px 30px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    display: inline-block; 
                    margin: 10px 5px; 
                }
                .btn:hover { background-color: #2980b9; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="success">Success: Appointment Booked</h2>
                <p>Appointment has been successfully booked.</p>
                <a href="/appointment" class="btn">Book Another Appointment</a>
                <a href="/" class="btn">Main Menu</a>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f'''<!DOCTYPE html>
        <html>
        <head>
            <title>Error - Appointment Booking</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }}
                .error {{ color: #e74c3c; font-size: 18px; }}
                .btn {{ 
                    background-color: #3498db; 
                    color: white; 
                    padding: 12px 30px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    display: inline-block; 
                    margin: 10px 5px; 
                }}
                .btn:hover {{ background-color: #2980b9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="error">Error: {str(e)}</h2>
                <a href="/appointment" class="btn">Back to Appointment Booking</a>
                <a href="/" class="btn">Main Menu</a>
            </div>
        </body>
        </html>
        '''

# Patient Billing Form
@app.route('/billing')
def billing():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Patient Billing - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                position: relative; overflow-x: hidden;
            }
            body::before {
                content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="20" y="20" width="60" height="60" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="2"/></svg>');
                background-size: 120px 120px; animation: float 15s linear infinite;
            }
            @keyframes float { 0% { transform: translateY(0); } 100% { transform: translateY(-120px); } }
            .header {
                background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1); padding: 20px 0; position: relative; z-index: 10;
            }
            .header-content {
                max-width: 1200px; margin: 0 auto; padding: 0 20px;
                display: flex; align-items: center; justify-content: space-between;
            }
            .logo-section { display: flex; align-items: center; gap: 15px; }
            .hospital-logo {
                width: 60px; height: 60px;
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                border-radius: 15px; display: flex; align-items: center; justify-content: center;
                font-size: 30px; box-shadow: 0 4px 15px rgba(250, 112, 154, 0.3);
            }
            .page-title h1 { color: #2c3e50; font-size: 28px; font-weight: 700; margin-bottom: 5px; }
            .page-title p { color: #7f8c8d; font-size: 14px; }
            .main-container {
                max-width: 1200px; margin: 0 auto; padding: 40px 20px; position: relative; z-index: 5;
            }
            .form-card {
                background: white; border-radius: 20px; padding: 50px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2); position: relative; overflow: hidden;
            }
            .form-card::before {
                content: ''; position: absolute; top: 0; left: 0; right: 0; height: 6px;
                background: linear-gradient(90deg, #fa709a 0%, #fee140 100%);
            }
            .section-header { text-align: center; margin-bottom: 40px; }
            .section-icon {
                width: 80px; height: 80px; margin: 0 auto 20px;
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                border-radius: 20px; display: flex; align-items: center; justify-content: center;
                font-size: 36px; color: white; box-shadow: 0 10px 30px rgba(250, 112, 154, 0.3);
                animation: pulse-icon 2s ease-in-out infinite;
            }
            @keyframes pulse-icon { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
            .section-header h2 { color: #2c3e50; font-size: 32px; font-weight: 700; margin-bottom: 10px; }
            .section-header p { color: #7f8c8d; font-size: 15px; }
            .summary-box {
                background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
                border-left: 4px solid #ff9800; padding: 20px; border-radius: 10px;
                margin-bottom: 30px; display: flex; align-items: center; gap: 15px;
            }
            .summary-box i { font-size: 28px; color: #f57c00; }
            .summary-box p { color: #e65100; font-size: 14px; margin: 0; }
            .form-grid {
                display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 25px; margin-bottom: 30px;
            }
            .form-group { position: relative; }
            .form-group label {
                display: flex; align-items: center; gap: 8px;
                margin-bottom: 10px; font-weight: 600; color: #2c3e50; font-size: 14px;
            }
            .form-group label i { color: #fa709a; font-size: 16px; }
            .form-group input {
                width: 100%; padding: 14px 18px; border: 2px solid #e0e0e0;
                border-radius: 10px; font-size: 14px; font-family: 'Poppins', sans-serif;
                transition: all 0.3s ease;
            }
            .form-group input:focus {
                outline: none; border-color: #fa709a;
                box-shadow: 0 0 0 4px rgba(250, 112, 154, 0.1);
            }
            .card-section {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 25px; border-radius: 15px; margin-bottom: 25px;
                border: 2px solid #dee2e6;
            }
            .card-section h3 {
                color: #2c3e50; font-size: 18px; margin-bottom: 20px;
                display: flex; align-items: center; gap: 10px;
            }
            .card-section h3 i { color: #fa709a; }
            .form-actions {
                display: flex; gap: 15px; justify-content: center;
                margin-top: 40px; padding-top: 30px; border-top: 2px solid #f0f0f0;
            }
            .btn {
                padding: 14px 35px; border-radius: 10px; font-size: 16px; font-weight: 600;
                text-decoration: none; display: inline-flex; align-items: center; gap: 10px;
                transition: all 0.3s ease; cursor: pointer; border: none;
                font-family: 'Poppins', sans-serif;
            }
            .update-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
            }
            .update-btn:hover { transform: translateY(-3px); box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4); }
            .generate-btn {
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                color: white; box-shadow: 0 8px 20px rgba(250, 112, 154, 0.3);
            }
            .generate-btn:hover { transform: translateY(-3px); box-shadow: 0 12px 30px rgba(250, 112, 154, 0.4); }
            .back-btn {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #2c3e50; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .back-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
            @media (max-width: 768px) {
                .form-card { padding: 30px 20px; }
                .form-grid { grid-template-columns: 1fr; }
                .form-actions { flex-direction: column; }
                .btn { width: 100%; justify-content: center; }
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">🏥</div>
                    <div class="page-title">
                        <h1>Patient Billing</h1>
                        <p>Generate and manage patient bills</p>
                    </div>
                </div>
            </div>
        </header>
        <div class="main-container">
            <div class="form-card">
                <div class="section-header">
                    <div class="section-icon"><i class="fas fa-file-invoice-dollar"></i></div>
                    <h2>Billing Information</h2>
                    <p>Enter treatment and medicine details to generate bill</p>
                </div>
                <div class="summary-box">
                    <i class="fas fa-info-circle"></i>
                    <p><strong>Note:</strong> Update discharge date first before generating the final bill. All amounts are in INR (₹).</p>
                </div>
                <form action="/billing/submit" method="POST">
                    <div class="card-section">
                        <h3><i class="fas fa-user-injured"></i> Patient Information</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="pat_id"><i class="fas fa-id-card"></i> Patient ID *</label>
                                <input type="number" id="pat_id" name="pat_id" placeholder="Enter patient ID" required>
                            </div>
                            <div class="form-group">
                                <label for="date_discharged"><i class="fas fa-calendar-times"></i> Date Discharged</label>
                                <input type="date" id="date_discharged" name="date_discharged">
                            </div>
                            <div class="form-group">
                                <button type="submit" name="action" value="update_date" class="btn update-btn">
                                    <i class="fas fa-sync-alt"></i> Update Discharge Date
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="card-section">
                        <h3><i class="fas fa-stethoscope"></i> Treatment Details</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="treatment"><i class="fas fa-heartbeat"></i> Treatment *</label>
                                <input type="text" id="treatment" name="treatment" placeholder="Treatment name/procedure" required>
                            </div>
                            <div class="form-group">
                                <label for="treatment_code"><i class="fas fa-barcode"></i> Treatment Code *</label>
                                <input type="text" id="treatment_code" name="treatment_code" placeholder="e.g., TRT001" required>
                            </div>
                            <div class="form-group">
                                <label for="treatment_cost"><i class="fas fa-rupee-sign"></i> Treatment Cost (₹) *</label>
                                <input type="number" id="treatment_cost" name="treatment_cost" placeholder="Enter cost" required>
                            </div>
                        </div>
                    </div>
                    <div class="card-section">
                        <h3><i class="fas fa-pills"></i> Medicine Details</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="medicine"><i class="fas fa-capsules"></i> Medicine Name *</label>
                                <input type="text" id="medicine" name="medicine" placeholder="Medicine name" required>
                            </div>
                            <div class="form-group">
                                <label for="medicine_qty"><i class="fas fa-box"></i> Quantity *</label>
                                <input type="number" id="medicine_qty" name="medicine_qty" placeholder="Number of units" required>
                            </div>
                            <div class="form-group">
                                <label for="medicine_price"><i class="fas fa-tag"></i> Price per Unit (₹) *</label>
                                <input type="number" id="medicine_price" name="medicine_price" placeholder="Price per unit" required>
                            </div>
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="submit" name="action" value="update_data" class="btn update-btn">
                            <i class="fas fa-save"></i> Update Data
                        </button>
                        <button type="submit" name="action" value="generate_bill" class="btn generate-btn">
                            <i class="fas fa-file-invoice"></i> Generate Bill
                        </button>
                        <a href="/" class="btn back-btn">
                            <i class="fas fa-arrow-left"></i> Back to Dashboard
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/billing/submit', methods=['POST'])
def billing_submit():
    try:
        action = request.form['action']
        pat_id = request.form['pat_id']
        
        conn = get_db_connection()
        
        if action == 'update_date':
            date_discharged = request.form['date_discharged']
            
            # Update discharge date in ROOM table
            conn.execute("UPDATE ROOM SET DATE_DISCHARGED=? WHERE PATIENT_ID=?", (date_discharged, pat_id))
            conn.commit()
            conn.close()
            
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Success - Update Discharge Date</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
                    .success { color: #27ae60; font-size: 18px; }
                    .btn { 
                        background-color: #3498db; 
                        color: white; 
                        padding: 12px 30px; 
                        text-decoration: none; 
                        border-radius: 5px; 
                        display: inline-block; 
                        margin: 10px 5px; 
                    }
                    .btn:hover { background-color: #2980b9; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2 class="success">Success: Discharge Date Updated</h2>
                    <p>Discharge date has been successfully updated.</p>
                    <a href="/billing" class="btn">Back to Billing</a>
                    <a href="/" class="btn">Main Menu</a>
                </div>
            </body>
            </html>
            '''
        
        elif action == 'update_data':
            treatment = request.form['treatment']
            treatment_code = request.form['treatment_code']
            treatment_cost = request.form['treatment_cost']
            medicine = request.form['medicine']
            medicine_qty = request.form['medicine_qty']
            medicine_price = request.form['medicine_price']
            
            # Check if patient is already registered in TREATMENT table
            existing_treatment = conn.execute('SELECT * FROM TREATMENT WHERE PATIENT_ID = ?', (pat_id,)).fetchone()
            if existing_treatment:
                conn.close()
                return '''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Error - Update Data</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
                        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
                        .error { color: #e74c3c; font-size: 18px; }
                        .btn { 
                            background-color: #3498db; 
                            color: white; 
                            padding: 12px 30px; 
                            text-decoration: none; 
                            border-radius: 5px; 
                            display: inline-block; 
                            margin: 10px 5px; 
                        }
                        .btn:hover { background-color: #2980b9; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2 class="error">Error: Patient Already Registered</h2>
                        <p>Patient ID is already registered in the treatment records.</p>
                        <a href="/billing" class="btn">Back to Billing</a>
                        <a href="/" class="btn">Main Menu</a>
                    </div>
                </body>
                </html>
                '''
            
            # Insert treatment and medicine data
            conn.execute('''INSERT INTO TREATMENT (PATIENT_ID, TREATMENT, TREATMENT_CODE, T_COST) 
                          VALUES (?, ?, ?, ?)''', 
                          (pat_id, treatment, treatment_code, treatment_cost))
            
            conn.execute('''INSERT INTO MEDICINE (PATIENT_ID, MEDICINE_NAME, M_COST, M_QTY) 
                          VALUES (?, ?, ?, ?)''', 
                          (pat_id, medicine, medicine_price, medicine_qty))
            
            conn.commit()
            conn.close()
            
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Success - Update Data</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
                    .success { color: #27ae60; font-size: 18px; }
                    .btn { 
                        background-color: #3498db; 
                        color: white; 
                        padding: 12px 30px; 
                        text-decoration: none; 
                        border-radius: 5px; 
                        display: inline-block; 
                        margin: 10px 5px; 
                    }
                    .btn:hover { background-color: #2980b9; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2 class="success">Success: Billing Data Saved</h2>
                    <p>Billing data has been successfully saved.</p>
                    <a href="/billing" class="btn">Back to Billing</a>
                    <a href="/" class="btn">Main Menu</a>
                </div>
            </body>
            </html>
            '''
        
        elif action == 'generate_bill':
            # Calculate total bill with proper error handling
            try:
                # Get treatment cost
                treatment_result = conn.execute('SELECT T_COST FROM TREATMENT WHERE PATIENT_ID = ?', (pat_id,)).fetchone()
                treatment_cost = treatment_result['T_COST'] if treatment_result else 0
                
                # Get medicine cost (price * quantity)
                medicine_result = conn.execute('SELECT M_COST, M_QTY FROM MEDICINE WHERE PATIENT_ID = ?', (pat_id,)).fetchone()
                medicine_total = 0
                if medicine_result:
                    medicine_total = medicine_result['M_COST'] * medicine_result['M_QTY']
                
                # Get room charges (calculate days stayed * rate)
                room_result = conn.execute('SELECT DATE_ADMITTED, DATE_DISCHARGED, RATE FROM ROOM WHERE PATIENT_ID = ?', (pat_id,)).fetchone()
                room_charges = 0
                days_stayed = 1
                if room_result:
                    if room_result['DATE_DISCHARGED'] and room_result['DATE_ADMITTED']:
                        from datetime import datetime
                        admitted = datetime.strptime(room_result['DATE_ADMITTED'], '%Y-%m-%d')
                        discharged = datetime.strptime(room_result['DATE_DISCHARGED'], '%Y-%m-%d')
                        days_stayed = max(1, (discharged - admitted).days)
                    room_charges = days_stayed * room_result['RATE']
                
                # Calculate total
                total_amount = treatment_cost + medicine_total + room_charges
                
                conn.close()
                
                return f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Bill Generated - Hospital Management System</title>
                    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                    <style>
                        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                        body {{
                            font-family: 'Poppins', sans-serif;
                            min-height: 100vh;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            padding: 20px;
                        }}
                        .bill-container {{
                            background: white;
                            border-radius: 20px;
                            padding: 50px;
                            max-width: 700px;
                            width: 100%;
                            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                            position: relative;
                            overflow: hidden;
                        }}
                        .bill-container::before {{
                            content: '';
                            position: absolute;
                            top: 0;
                            left: 0;
                            right: 0;
                            height: 6px;
                            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                        }}
                        .header {{
                            text-align: center;
                            margin-bottom: 30px;
                        }}
                        .success-icon {{
                            width: 80px;
                            height: 80px;
                            margin: 0 auto 20px;
                            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 40px;
                            color: white;
                            animation: bounce 1s ease-in-out;
                        }}
                        @keyframes bounce {{
                            0%, 100% {{ transform: scale(1); }}
                            50% {{ transform: scale(1.1); }}
                        }}
                        .header h1 {{
                            color: #2c3e50;
                            font-size: 28px;
                            font-weight: 700;
                            margin-bottom: 10px;
                        }}
                        .header p {{
                            color: #7f8c8d;
                            font-size: 14px;
                        }}
                        .patient-info {{
                            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                            padding: 20px;
                            border-radius: 15px;
                            margin-bottom: 25px;
                            text-align: center;
                        }}
                        .patient-info h2 {{
                            color: #2c3e50;
                            font-size: 18px;
                            margin-bottom: 5px;
                        }}
                        .patient-info p {{
                            color: #555;
                            font-size: 14px;
                        }}
                        .bill-breakdown {{
                            background: #f8f9fa;
                            padding: 25px;
                            border-radius: 15px;
                            margin-bottom: 25px;
                        }}
                        .breakdown-item {{
                            display: flex;
                            justify-content: space-between;
                            padding: 12px 0;
                            border-bottom: 1px solid #dee2e6;
                        }}
                        .breakdown-item:last-child {{
                            border-bottom: none;
                        }}
                        .breakdown-label {{
                            color: #555;
                            font-size: 14px;
                            display: flex;
                            align-items: center;
                            gap: 10px;
                        }}
                        .breakdown-label i {{
                            color: #667eea;
                            width: 20px;
                        }}
                        .breakdown-value {{
                            color: #2c3e50;
                            font-weight: 600;
                            font-size: 14px;
                        }}
                        .total-section {{
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 25px;
                            border-radius: 15px;
                            text-align: center;
                            color: white;
                            margin-bottom: 25px;
                        }}
                        .total-label {{
                            font-size: 16px;
                            margin-bottom: 10px;
                            opacity: 0.9;
                        }}
                        .total-amount {{
                            font-size: 42px;
                            font-weight: 700;
                            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                        }}
                        .actions {{
                            display: flex;
                            gap: 15px;
                            justify-content: center;
                        }}
                        .btn {{
                            padding: 14px 35px;
                            border-radius: 10px;
                            font-size: 16px;
                            font-weight: 600;
                            text-decoration: none;
                            display: inline-flex;
                            align-items: center;
                            gap: 10px;
                            transition: all 0.3s ease;
                            cursor: pointer;
                            border: none;
                            font-family: 'Poppins', sans-serif;
                        }}
                        .back-billing-btn {{
                            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                            color: #2c3e50;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                        }}
                        .back-billing-btn:hover {{
                            transform: translateY(-2px);
                            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
                        }}
                        .dashboard-btn {{
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                        }}
                        .dashboard-btn:hover {{
                            transform: translateY(-2px);
                            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
                        }}
                        @media (max-width: 768px) {{
                            .bill-container {{
                                padding: 30px 20px;
                            }}
                            .actions {{
                                flex-direction: column;
                            }}
                            .btn {{
                                width: 100%;
                                justify-content: center;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="bill-container">
                        <div class="header">
                            <div class="success-icon">
                                <i class="fas fa-check"></i>
                            </div>
                            <h1>Bill Generated Successfully!</h1>
                            <p>Patient ID: {pat_id}</p>
                        </div>
                        
                        <div class="patient-info">
                            <h2><i class="fas fa-file-invoice"></i> Bill Summary</h2>
                            <p>Detailed breakdown of charges</p>
                        </div>
                        
                        <div class="bill-breakdown">
                            <div class="breakdown-item">
                                <div class="breakdown-label">
                                    <i class="fas fa-stethoscope"></i>
                                    Treatment Cost
                                </div>
                                <div class="breakdown-value">₹{treatment_cost:.2f}</div>
                            </div>
                            <div class="breakdown-item">
                                <div class="breakdown-label">
                                    <i class="fas fa-pills"></i>
                                    Medicine Charges
                                </div>
                                <div class="breakdown-value">₹{medicine_total:.2f}</div>
                            </div>
                            <div class="breakdown-item">
                                <div class="breakdown-label">
                                    <i class="fas fa-bed"></i>
                                    Room Charges ({days_stayed} days)
                                </div>
                                <div class="breakdown-value">₹{room_charges:.2f}</div>
                            </div>
                            <div class="breakdown-item" style="border-top: 2px solid #667eea; margin-top: 15px; padding-top: 15px;">
                                <div class="breakdown-label" style="font-size: 16px; font-weight: 700; color: #667eea;">
                                    <i class="fas fa-calculator"></i>
                                    TOTAL AMOUNT
                                </div>
                                <div class="breakdown-value" style="font-size: 20px; color: #667eea;">₹{total_amount:.2f}</div>
                            </div>
                        </div>
                        
                        <div class="total-section">
                            <div class="total-label">Grand Total</div>
                            <div class="total-amount">₹{total_amount:.2f}</div>
                        </div>
                        
                        <div class="actions">
                            <a href="/billing" class="btn back-billing-btn">
                                <i class="fas fa-arrow-left"></i>
                                Back to Billing
                            </a>
                            <a href="/" class="btn dashboard-btn">
                                <i class="fas fa-home"></i>
                                Go to Dashboard
                            </a>
                        </div>
                    </div>
                </body>
                </html>
                '''
            except Exception as e:
                conn.close()
                return f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Error - Bill Generation</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }}
                        .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }}
                        .error {{ color: #e74c3c; font-size: 18px; }}
                        .btn {{ 
                            background-color: #3498db; 
                            color: white; 
                            padding: 12px 30px; 
                            text-decoration: none; 
                            border-radius: 5px; 
                            display: inline-block; 
                            margin: 10px 5px; 
                        }}
                        .btn:hover {{ background-color: #2980b9; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2 class="error">Error Generating Bill</h2>
                        <p>Please ensure all required data is entered: patient must have room allocation, treatment, and medicine records.</p>
                        <p style="color: #7f8c8d; font-size: 12px; margin-top: 10px;">Details: {str(e)}</p>
                        <a href="/billing" class="btn">Back to Billing</a>
                        <a href="/" class="btn">Main Menu</a>
                    </div>
                </body>
                </html>
                '''
        
        else:
            conn.close()
            return '''<!DOCTYPE html>
            <html>
            <head>
                <title>Error - Invalid Action</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
                    .error { color: #e74c3c; font-size: 18px; }
                    .btn { 
                        background-color: #3498db; 
                        color: white; 
                        padding: 12px 30px; 
                        text-decoration: none; 
                        border-radius: 5px; 
                        display: inline-block; 
                        margin: 10px 5px; 
                    }
                    .btn:hover { background-color: #2980b9; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2 class="error">Error: Invalid Action</h2>
                    <a href="/billing" class="btn">Back to Billing</a>
                    <a href="/" class="btn">Main Menu</a>
                </div>
            </body>
            </html>
            '''
    except Exception as e:
        return f'''<!DOCTYPE html>
        <html>
        <head>
            <title>Error - Billing</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }}
                .error {{ color: #e74c3c; font-size: 18px; }}
                .btn {{ 
                    background-color: #3498db; 
                    color: white; 
                    padding: 12px 30px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    display: inline-block; 
                    margin: 10px 5px; 
                }}
                .btn:hover {{ background-color: #2980b9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="error">Error: {str(e)}</h2>
                <a href="/billing" class="btn">Back to Billing</a>
                <a href="/" class="btn">Main Menu</a>
            </div>
        </body>
        </html>
        '''

# AI Medical Assistant Route
@app.route('/ai-assistant')
def ai_assistant():
    return ai_assistant_page()

# Nurse Management Route
@app.route('/nurse')
def nurse_management():
    return nurse_page()

# View Nurses Route
@app.route('/view-nurses')
def view_nurses():
    return view_nurses_page()

def ai_assistant_page():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Medical Assistant - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                padding: 20px;
            }
            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                border-radius: 15px;
                padding: 20px 30px;
                margin-bottom: 30px;
            }
            .header-content {
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .logo-section {
                display: flex;
                align-items: center;
                gap: 20px;
            }
            .hospital-logo {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 30px;
                color: white;
            }
            h1 {
                color: #2c3e50;
                font-size: 28px;
            }
            .back-btn {
                background-color: #3498db;
                color: white;
                padding: 12px 25px;
                text-decoration: none;
                border-radius: 8px;
                transition: all 0.3s;
            }
            .back-btn:hover {
                background-color: #2980b9;
                transform: translateY(-2px);
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .form-card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 20px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            }
            .form-group {
                margin-bottom: 25px;
            }
            label {
                display: block;
                color: #2c3e50;
                font-weight: 600;
                margin-bottom: 10px;
                font-size: 16px;
            }
            textarea {
                width: 100%;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-family: 'Poppins', sans-serif;
                font-size: 14px;
                resize: vertical;
                transition: border-color 0.3s;
            }
            textarea:focus {
                outline: none;
                border-color: #11998e;
            }
            .button-group {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
            }
            .btn {
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                display: inline-flex;
                align-items: center;
                gap: 10px;
            }
            .btn-analyze {
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                color: white;
                flex: 1;
            }
            .btn-analyze:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(17, 153, 142, 0.4);
            }
            .btn-clear {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
            }
            .btn-clear:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(245, 87, 108, 0.4);
            }
            .btn-exit {
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                color: white;
            }
            .btn-exit:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(250, 112, 154, 0.4);
            }
            .result-card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            }
            .result-header {
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #e0e0e0;
            }
            .result-content {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #11998e;
                white-space: pre-wrap;
                font-size: 14px;
                line-height: 1.8;
                color: #2c3e50;
            }
            .loading {
                text-align: center;
                padding: 40px;
                color: #11998e;
                font-size: 18px;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #11998e;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .disclaimer {
                background: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 10px;
                padding: 15px;
                margin-top: 20px;
                font-size: 13px;
                color: #856404;
            }
            @media (max-width: 768px) {
                .button-group {
                    flex-direction: column;
                }
                .btn {
                    width: 100%;
                }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div>
                        <h1>🤖 AI Medical Assistant</h1>
                        <p style="color: #7f8c8d;">Instant Medical Information & Guidance</p>
                    </div>
                </div>
                <a href="/" class="back-btn">
                    <i class="fas fa-arrow-left"></i>
                    Back to Dashboard
                </a>
            </div>
        </div>

        <div class="container">
            <div class="form-card">
                <form id="aiForm" onsubmit="return analyzeDisease();">
                    <div class="form-group">
                        <label for="diseaseDesc">
                            <i class="fas fa-stethoscope"></i>
                            Disease Name / Symptoms Description:
                        </label>
                        <textarea id="diseaseDesc" name="diseaseDesc" rows="4" 
                                  placeholder="Enter the disease name or describe your symptoms..." required></textarea>
                    </div>

                    <div class="form-group">
                        <label for="additionalSymptoms">
                            <i class="fas fa-notes-medical"></i>
                            Additional Symptoms (Optional):
                        </label>
                        <textarea id="additionalSymptoms" name="additionalSymptoms" rows="3"
                                  placeholder="Any other symptoms or relevant information..."></textarea>
                    </div>

                    <div class="button-group">
                        <button type="submit" class="btn btn-analyze">
                            <i class="fas fa-search"></i>
                            Analyze with AI
                        </button>
                        <button type="button" class="btn btn-clear" onclick="clearForm()">
                            <i class="fas fa-redo"></i>
                            Clear
                        </button>
                        <button type="button" class="btn btn-exit" onclick="window.location.href='/';">
                            <i class="fas fa-sign-out-alt"></i>
                            Exit
                        </button>
                    </div>
                </form>
            </div>

            <div class="result-card" id="resultCard" style="display: none;">
                <div class="result-header">
                    <i class="fas fa-file-medical" style="font-size: 30px; color: #11998e;"></i>
                    <h2>AI Analysis Result</h2>
                </div>
                <div class="result-content" id="resultContent"></div>
                <div class="disclaimer">
                    <strong>⚠️ MEDICAL DISCLAIMER:</strong> This AI-generated information is for educational purposes only and does not replace professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers.
                </div>
            </div>
        </div>

        <!-- Modal for Results -->
        <div id="resultModal" class="modal" style="display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.5);">
            <div style="background: white; margin: 5% auto; padding: 0; border-radius: 15px; width: 80%; max-width: 900px; box-shadow: 0 10px 40px rgba(0,0,0,0.3);">
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 30px; border-bottom: 2px solid #e0e0e0; border-radius: 15px 15px 0 0;">
                    <h2 id="modalTitle" style="margin: 0; color: #11998e;">🏥 AI Medical Analysis Report</h2>
                    <button onclick="closeModal()" style="background: none; border: none; font-size: 30px; cursor: pointer; color: #999;">&times;</button>
                </div>
                <div style="padding: 30px; max-height: 70vh; overflow-y: auto;" id="modalContent">
                    <!-- Content will be loaded here -->
                </div>
                <div style="padding: 15px 30px; border-top: 2px solid #e0e0e0; text-align: center; background: #f8f9fa; border-radius: 0 0 15px 15px;">
                    <button onclick="closeModal()" style="padding: 12px 30px; background: #6c757d; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin: 5px;">Close</button>
                    <button onclick="clearForm()" style="padding: 12px 30px; background: #11998e; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin: 5px;">Clear & New Search</button>
                </div>
            </div>
        </div>

        <script>
            function analyzeDisease() {
                const diseaseDesc = document.getElementById('diseaseDesc').value;
                const additionalSymptoms = document.getElementById('additionalSymptoms').value;
                
                if (!diseaseDesc.trim()) {
                    alert('Please enter disease name or symptoms');
                    return false;
                }

                // Show loading modal
                showModal('Analyzing...', `
                    <div class="loading">
                        <div class="spinner"></div>
                        <p>Fetching data from medical databases...</p>
                    </div>
                `);

                // Fetch real data from APIs
                fetchMedicalData(diseaseDesc, additionalSymptoms);

                return false;
            }

            function showModal(title, content) {
                const modal = document.getElementById('resultModal');
                document.getElementById('modalTitle').textContent = title;
                document.getElementById('modalContent').innerHTML = content;
                modal.style.display = 'block';
            }

            function closeModal() {
                document.getElementById('resultModal').style.display = 'none';
            }

            function clearForm() {
                document.getElementById('diseaseDesc').value = '';
                document.getElementById('additionalSymptoms').value = '';
                closeModal();
            }

            async function fetchMedicalData(disease, symptoms) {
                try {
                    // Fetch from Wikipedia
                    const wikiData = await fetchFromWikipedia(disease);
                    
                    // Generate report
                    const report = generateReport(disease, symptoms, wikiData);
                    
                    // Display in modal
                    showModal('🏥 AI Medical Analysis Report', report);
                } catch (error) {
                    showModal('Error', `<p style="color: red;">Error: ${error.message}</p>`);
                }
            }

            async function fetchFromWikipedia(query) {
                const url = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(query)}`;
                const headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Accept': 'application/json'
                };
                
                try {
                    const response = await fetch(url, { headers });
                    if (response.ok) {
                        return await response.json();
                    }
                } catch (e) {
                    console.log('Wikipedia fetch error:', e);
                }
                return null;
            }

            function generateReport(disease, symptoms, wikiData) {
                let html = `
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #11998e;">
                        <h3 style="color: #11998e; margin-bottom: 15px;">📋 Condition: ${disease.toUpperCase()}</h3>
                `;
                
                if (symptoms) {
                    html += `<p><strong>➕ Symptoms:</strong> ${symptoms}</p>`;
                }
                
                if (wikiData && wikiData.extract) {
                    html += `
                        <div style="margin: 20px 0;">
                            <h4 style="color: #2c3e50;">📖 Information from Wikipedia:</h4>
                            <p style="line-height: 1.8; color: #555;">${wikiData.extract}</p>
                            ${wikiData.content_urls && wikiData.content_urls.desktop ? 
                                `<a href="${wikiData.content_urls.desktop.page}" target="_blank" 
                                   style="display: inline-block; margin-top: 10px; padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px;">
                                    📄 Read More on Wikipedia
                                </a>` : ''}
                        </div>
                    `;
                }
                
                // Add precautions
                html += `
                    <div style="margin: 20px 0; padding: 15px; background: #fff3cd; border-radius: 8px;">
                        <h4 style="color: #856404;">✅ Recommended Precautions:</h4>
                        <ul style="line-height: 2; color: #856404;">
                            <li>Rest and get adequate sleep</li>
                            <li>Stay hydrated by drinking plenty of fluids</li>
                            <li>Maintain proper hygiene</li>
                            <li>Eat nutritious food</li>
                            <li>Avoid stress</li>
                            <li>Monitor your symptoms</li>
                            <li>Consult a doctor if symptoms persist</li>
                        </ul>
                    </div>
                `;
                
                // Add medicine info
                html += `
                    <div style="margin: 20px 0; padding: 15px; background: #d1ecf1; border-radius: 8px;">
                        <h4 style="color: #0c5460;">💊 Common Medicine Categories:</h4>
                        <p style="line-height: 1.8; color: #0c5460;">
                            <strong>Note:</strong> Always consult a doctor before taking any medication.<br><br>
                            • <strong>Pain/Fever:</strong> Acetaminophen, Ibuprofen<br>
                            • <strong>Infection:</strong> Antibiotics (prescription only)<br>
                            • <strong>Allergy:</strong> Antihistamines<br>
                            • <strong>Inflammation:</strong> NSAIDs<br>
                            • <strong>General wellness:</strong> Multivitamins
                        </p>
                    </div>
                `;
                
                // Emergency contacts
                html += `
                    <div style="margin: 20px 0; padding: 15px; background: #f8d7da; border-radius: 8px; border-left: 5px solid #dc3545;">
                        <h4 style="color: #721c24;">📞 Emergency Contacts:</h4>
                        <p style="line-height: 1.8; color: #721c24;">
                            <strong>Emergency Services:</strong> 911 (US) / 112 (EU) / 108 (India)<br>
                            <strong>Poison Control:</strong> 1-800-222-1222<br>
                            <strong>Mental Health:</strong> 988 (US)
                        </p>
                    </div>
                `;
                
                // Disclaimer
                html += `
                    <div style="margin-top: 20px; padding: 15px; background: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; text-align: center;">
                        <strong style="color: #856404;">⚠️ MEDICAL DISCLAIMER:</strong><br>
                        <span style="color: #856404; font-size: 13px; line-height: 1.6;">
                            This information is for educational purposes only and does NOT replace professional medical advice.
                            Always consult qualified healthcare providers for diagnosis and treatment.
                        </span>
                    </div>
                `;
                
                html += `</div>`;
                return html;
            }

            // Close modal when clicking outside
            window.onclick = function(event) {
                const modal = document.getElementById('resultModal');
                if (event.target == modal) {
                    closeModal();
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/exit')
def exit_app():
    return '<h2>Goodbye!</h2><p>The application has been closed.</p><a href="/">Back to Main Menu</a>'

# Route to view all patient data
@app.route('/patients')
def view_patients():
    conn = get_db_connection()
    patients = conn.execute('''SELECT p.PATIENT_ID, p.NAME, p.SEX, p.BLOOD_GROUP, p.DOB, p.ADDRESS, p.CONSULT_TEAM, p.EMAIL, c.CONTACTNO, c.ALT_CONTACT 
                           FROM PATIENT p 
                           LEFT JOIN CONTACT_NO c ON p.PATIENT_ID = c.PATIENT_ID''').fetchall()
    conn.close()
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>View Patients - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
            }
            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                padding: 20px 0;
                margin-bottom: 30px;
            }
            .header-content {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .logo-section { display: flex; align-items: center; gap: 15px; }
            .hospital-logo {
                width: 60px; height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                display: flex; align-items: center; justify-content: center;
                font-size: 30px;
            }
            .page-title h1 { color: #2c3e50; font-size: 28px; font-weight: 700; }
            .page-title p { color: #7f8c8d; font-size: 14px; }
            .main-container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
            }
            .stat-number { font-size: 32px; font-weight: 700; color: #667eea; margin-bottom: 5px; }
            .stat-label { color: #7f8c8d; font-size: 13px; }
            .table-container {
                overflow-x: auto;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            table { width: 100%; border-collapse: collapse; }
            thead {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            th { padding: 18px 12px; font-weight: 600; text-align: left; font-size: 14px; }
            tbody tr {
                transition: all 0.3s ease;
                border-bottom: 1px solid #e0e0e0;
            }
            tbody tr:hover {
                background-color: #f8f9fa;
                transform: scale(1.01);
            }
            td { padding: 14px 12px; font-size: 13px; color: #555; }
            .actions {
                text-align: center;
                margin-top: 30px;
            }
            .btn {
                padding: 14px 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                display: inline-flex;
                align-items: center;
                gap: 10px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            @media (max-width: 768px) {
                .main-container { padding: 20px; }
                th, td { padding: 10px 8px; font-size: 12px; }
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">🏥</div>
                    <div class="page-title">
                        <h1>Patient Records</h1>
                        <p>Complete list of registered patients</p>
                    </div>
                </div>
            </div>
        </header>
        <div class="main-container">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">''' + str(len(patients)) + '''</div>
                    <div class="stat-label"><i class="fas fa-users"></i> Total Patients</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><i class="fas fa-heartbeat" style="color: #667eea;"></i></div>
                    <div class="stat-label">Active Care</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><i class="fas fa-user-md" style="color: #667eea;"></i></div>
                    <div class="stat-label">Doctors Assigned</div>
                </div>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th><i class="fas fa-id-card"></i> ID</th>
                            <th><i class="fas fa-user"></i> Name</th>
                            <th><i class="fas fa-venus-mars"></i> Sex</th>
                            <th><i class="fas fa-tint"></i> Blood Group</th>
                            <th><i class="fas fa-calendar-alt"></i> DOB</th>
                            <th><i class="fas fa-map-marker-alt"></i> Address</th>
                            <th><i class="fas fa-user-md"></i> Consult Team</th>
                            <th><i class="fas fa-envelope"></i> Email</th>
                            <th><i class="fas fa-phone"></i> Contact</th>
                        </tr>
                    </thead>
                    <tbody>
    ''' + ''.join([f'<tr><td>{p["PATIENT_ID"]}</td><td>{p["NAME"]}</td><td>{p["SEX"]}</td><td>{p["BLOOD_GROUP"]}</td><td>{p["DOB"]}</td><td>{p["ADDRESS"]}</td><td>{p["CONSULT_TEAM"]}</td><td>{p["EMAIL"]}</td><td>{p["CONTACTNO"]}</td></tr>' for p in patients]) + '''
                    </tbody>
                </table>
            </div>
            <div class="actions">
                <a href="/" class="btn">
                    <i class="fas fa-arrow-left"></i> Back to Dashboard
                </a>
            </div>
        </div>
    </body>
    </html>
    '''

# Route to view all employees
@app.route('/employees')
def view_employees():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM EMPLOYEE').fetchall()
    conn.close()
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>View Employees - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                padding: 20px;
            }
            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                padding: 20px 0;
                margin-bottom: 30px;
            }
            .header-content {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .logo-section { display: flex; align-items: center; gap: 15px; }
            .hospital-logo {
                width: 60px; height: 60px;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                border-radius: 15px;
                display: flex; align-items: center; justify-content: center;
                font-size: 30px;
            }
            .page-title h1 { color: #2c3e50; font-size: 28px; font-weight: 700; }
            .page-title p { color: #7f8c8d; font-size: 14px; }
            .main-container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
            }
            .stat-number { font-size: 32px; font-weight: 700; color: #4facfe; margin-bottom: 5px; }
            .stat-label { color: #7f8c8d; font-size: 13px; }
            .table-container {
                overflow-x: auto;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            table { width: 100%; border-collapse: collapse; }
            thead {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
            }
            th { padding: 18px 12px; font-weight: 600; text-align: left; font-size: 14px; }
            tbody tr {
                transition: all 0.3s ease;
                border-bottom: 1px solid #e0e0e0;
            }
            tbody tr:hover {
                background-color: #f8f9fa;
                transform: scale(1.01);
            }
            td { padding: 14px 12px; font-size: 13px; color: #555; }
            .actions {
                text-align: center;
                margin-top: 30px;
            }
            .btn {
                padding: 14px 40px;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                display: inline-flex;
                align-items: center;
                gap: 10px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
            }
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
            }
            @media (max-width: 768px) {
                .main-container { padding: 20px; }
                th, td { padding: 10px 8px; font-size: 12px; }
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">🏥</div>
                    <div class="page-title">
                        <h1>Hospital Staff Directory</h1>
                        <p>Complete list of hospital employees</p>
                    </div>
                </div>
            </div>
        </header>
        <div class="main-container">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">''' + str(len(employees)) + '''</div>
                    <div class="stat-label"><i class="fas fa-users"></i> Total Staff</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><i class="fas fa-user-md" style="color: #4facfe;"></i></div>
                    <div class="stat-label">Medical Team</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><i class="fas fa-hospital" style="color: #4facfe;"></i></div>
                    <div class="stat-label">All Departments</div>
                </div>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th><i class="fas fa-id-badge"></i> ID</th>
                            <th><i class="fas fa-user"></i> Name</th>
                            <th><i class="fas fa-venus-mars"></i> Gender</th>
                            <th><i class="fas fa-birthday-cake"></i> Age</th>
                            <th><i class="fas fa-briefcase"></i> Designation</th>
                            <th><i class="fas fa-rupee-sign"></i> Salary</th>
                            <th><i class="fas fa-medal"></i> Experience</th>
                            <th><i class="fas fa-envelope"></i> Email</th>
                            <th><i class="fas fa-phone"></i> Phone</th>
                        </tr>
                    </thead>
                    <tbody>
    ''' + ''.join([f'<tr><td>{e["EMP_ID"]}</td><td>{e["EMP_NAME"]}</td><td>{e["SEX"]}</td><td>{e["AGE"]}</td><td>{e["DESIG"]}</td><td>₹{e["SAL"]}</td><td>{e["EXP"]}</td><td>{e["EMAIL"]}</td><td>{e["PHONE"]}</td></tr>' for e in employees]) + '''
                    </tbody>
                </table>
            </div>
            <div class="actions">
                <a href="/" class="btn">
                    <i class="fas fa-arrow-left"></i> Back to Dashboard
                </a>
            </div>
        </div>
    </body>
    </html>
    '''

# Route to view all appointments
@app.route('/appointments')
def view_appointments():
    conn = get_db_connection()
    appointments = conn.execute('''SELECT a.AP_NO, a.PATIENT_ID, p.NAME as PATIENT_NAME, a.EMP_ID, e.EMP_NAME as DOCTOR_NAME, 
                                   a.AP_TIME, a.AP_DATE, a.DESCRIPTION 
                           FROM APPOINTMENT a 
                           LEFT JOIN PATIENT p ON a.PATIENT_ID = p.PATIENT_ID 
                           LEFT JOIN EMPLOYEE e ON a.EMP_ID = e.EMP_ID''').fetchall()
    conn.close()
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>View Appointments - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                padding: 20px;
            }
            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                padding: 20px 0;
                margin-bottom: 30px;
            }
            .header-content {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .logo-section { display: flex; align-items: center; gap: 15px; }
            .hospital-logo {
                width: 60px; height: 60px;
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                border-radius: 15px;
                display: flex; align-items: center; justify-content: center;
                font-size: 30px;
            }
            .page-title h1 { color: #2c3e50; font-size: 28px; font-weight: 700; }
            .page-title p { color: #7f8c8d; font-size: 14px; }
            .main-container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
            }
            .stat-number { font-size: 32px; font-weight: 700; color: #43e97b; margin-bottom: 5px; }
            .stat-label { color: #7f8c8d; font-size: 13px; }
            .table-container {
                overflow-x: auto;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            table { width: 100%; border-collapse: collapse; }
            thead {
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                color: white;
            }
            th { padding: 18px 12px; font-weight: 600; text-align: left; font-size: 14px; }
            tbody tr {
                transition: all 0.3s ease;
                border-bottom: 1px solid #e0e0e0;
            }
            tbody tr:hover {
                background-color: #f8f9fa;
                transform: scale(1.01);
            }
            td { padding: 14px 12px; font-size: 13px; color: #555; }
            .actions {
                text-align: center;
                margin-top: 30px;
            }
            .btn {
                padding: 14px 40px;
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                display: inline-flex;
                align-items: center;
                gap: 10px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(67, 233, 123, 0.3);
            }
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(67, 233, 123, 0.4);
            }
            @media (max-width: 768px) {
                .main-container { padding: 20px; }
                th, td { padding: 10px 8px; font-size: 12px; }
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">🏥</div>
                    <div class="page-title">
                        <h1>Appointment Schedule</h1>
                        <p>All scheduled consultations and meetings</p>
                    </div>
                </div>
            </div>
        </header>
        <div class="main-container">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">''' + str(len(appointments)) + '''</div>
                    <div class="stat-label"><i class="fas fa-calendar-check"></i> Total Appointments</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><i class="fas fa-user-injured" style="color: #43e97b;"></i></div>
                    <div class="stat-label">Patients Scheduled</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><i class="fas fa-stethoscope" style="color: #43e97b;"></i></div>
                    <div class="stat-label">Doctors Available</div>
                </div>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th><i class="fas fa-hashtag"></i> Appt No</th>
                            <th><i class="fas fa-id-card"></i> Patient ID</th>
                            <th><i class="fas fa-user"></i> Patient Name</th>
                            <th><i class="fas fa-user-md"></i> Doctor ID</th>
                            <th><i class="fas fa-user-md"></i> Doctor Name</th>
                            <th><i class="fas fa-clock"></i> Time</th>
                            <th><i class="fas fa-calendar-alt"></i> Date</th>
                            <th><i class="fas fa-comment-medical"></i> Description</th>
                        </tr>
                    </thead>
                    <tbody>
    ''' + ''.join([f'<tr><td>{a["AP_NO"]}</td><td>{a["PATIENT_ID"]}</td><td>{a["PATIENT_NAME"]}</td><td>{a["EMP_ID"]}</td><td>{a["DOCTOR_NAME"]}</td><td>{a["AP_TIME"]}</td><td>{a["AP_DATE"]}</td><td>{a["DESCRIPTION"]}</td></tr>' for a in appointments]) + '''
                    </tbody>
                </table>
            </div>
            <div class="actions">
                <a href="/" class="btn">
                    <i class="fas fa-arrow-left"></i> Back to Dashboard
                </a>
            </div>
        </div>
    </body>
    </html>
    '''

# Route to view all rooms
@app.route('/rooms')
def view_rooms():
    conn = get_db_connection()
    rooms = conn.execute('''SELECT r.PATIENT_ID, p.NAME as PATIENT_NAME, r.ROOM_NO, r.ROOM_TYPE, r.RATE, r.DATE_ADMITTED, r.DATE_DISCHARGED 
                           FROM ROOM r 
                           LEFT JOIN PATIENT p ON r.PATIENT_ID = p.PATIENT_ID''').fetchall()
    conn.close()
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>View Rooms - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                padding: 20px;
            }
            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                padding: 20px 0;
                margin-bottom: 30px;
            }
            .header-content {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .logo-section { display: flex; align-items: center; gap: 15px; }
            .hospital-logo {
                width: 60px; height: 60px;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 15px;
                display: flex; align-items: center; justify-content: center;
                font-size: 30px;
            }
            .page-title h1 { color: #2c3e50; font-size: 28px; font-weight: 700; }
            .page-title p { color: #7f8c8d; font-size: 14px; }
            .main-container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
            }
            .stat-number { font-size: 32px; font-weight: 700; color: #f093fb; margin-bottom: 5px; }
            .stat-label { color: #7f8c8d; font-size: 13px; }
            .table-container {
                overflow-x: auto;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            table { width: 100%; border-collapse: collapse; }
            thead {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
            }
            th { padding: 18px 12px; font-weight: 600; text-align: left; font-size: 14px; }
            tbody tr {
                transition: all 0.3s ease;
                border-bottom: 1px solid #e0e0e0;
            }
            tbody tr:hover {
                background-color: #f8f9fa;
                transform: scale(1.01);
            }
            td { padding: 14px 12px; font-size: 13px; color: #555; }
            .room-status {
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                display: inline-block;
            }
            .occupied {
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
                color: white;
            }
            .available {
                background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);
                color: white;
            }
            .actions {
                text-align: center;
                margin-top: 30px;
            }
            .btn {
                padding: 14px 40px;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                display: inline-flex;
                align-items: center;
                gap: 10px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
            }
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(240, 147, 251, 0.4);
            }
            @media (max-width: 768px) {
                .main-container { padding: 20px; }
                th, td { padding: 10px 8px; font-size: 12px; }
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">🏥</div>
                    <div class="page-title">
                        <h1>Room Allocation Status</h1>
                        <p>Current room occupancy and availability</p>
                    </div>
                </div>
            </div>
        </header>
        <div class="main-container">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">''' + str(len(rooms)) + '''</div>
                    <div class="stat-label"><i class="fas fa-bed"></i> Total Rooms</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><i class="fas fa-procedures" style="color: #f093fb;"></i></div>
                    <div class="stat-label">Occupied Rooms</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><i class="fas fa-door-open" style="color: #f093fb;"></i></div>
                    <div class="stat-label">Available Rooms</div>
                </div>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th><i class="fas fa-user-injured"></i> Patient ID</th>
                            <th><i class="fas fa-user"></i> Patient Name</th>
                            <th><i class="fas fa-hashtag"></i> Room No</th>
                            <th><i class="fas fa-door-open"></i> Room Type</th>
                            <th><i class="fas fa-rupee-sign"></i> Rate/Day</th>
                            <th><i class="fas fa-calendar-check"></i> Date Admitted</th>
                            <th><i class="fas fa-calendar-times"></i> Date Discharged</th>
                            <th><i class="fas fa-info-circle"></i> Status</th>
                        </tr>
                    </thead>
                    <tbody>
    ''' + ''.join([f'<tr><td>{r["PATIENT_ID"] or "N/A"}</td><td>{r["PATIENT_NAME"] or "Vacant"}</td><td>{r["ROOM_NO"]}</td><td>{r["ROOM_TYPE"]}</td><td>₹{r["RATE"]}</td><td>{r["DATE_ADMITTED"]}</td><td>{r["DATE_DISCHARGED"] or "Not Discharged"}</td><td><span class="room-status occupied">Occupied</span></td></tr>' for r in rooms]) + '''
                    </tbody>
                </table>
            </div>
            <div class="actions">
                <a href="/" class="btn">
                    <i class="fas fa-arrow-left"></i> Back to Dashboard
                </a>
            </div>
        </div>
    </body>
    </html>
    '''

# Add login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        # Validate input
        if not username or not password:
            return '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Login Error - Hospital Management System</title>
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
                <style>
                    * { margin: 0; padding: 0; box-sizing: border-box; }
                    body {
                        font-family: 'Poppins', sans-serif;
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 20px;
                    }
                    .error-container {
                        max-width: 450px;
                        width: 100%;
                        background: white;
                        border-radius: 20px;
                        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                        padding: 40px;
                        text-align: center;
                    }
                    .error-icon { font-size: 80px; margin-bottom: 20px; animation: shake 0.5s ease-in-out; }
                    @keyframes shake {
                        0%, 100% { transform: translateX(0); }
                        25% { transform: translateX(-10px); }
                        75% { transform: translateX(10px); }
                    }
                    h2 { color: #e74c3c; font-size: 28px; font-weight: 600; margin-bottom: 15px; }
                    p { color: #7f8c8d; font-size: 16px; margin-bottom: 30px; line-height: 1.6; }
                    .btn {
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white; padding: 14px 30px; text-decoration: none; border-radius: 8px;
                        display: inline-block; font-size: 16px; font-weight: 600;
                        transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                    }
                    .btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4); }
                </style>
            </head>
            <body>
                <div class="error-container">
                    <div class="error-icon">⚠️</div>
                    <h2>Please Fill All Fields</h2>
                    <p>Both username and password are required.<br>Please try again.</p>
                    <a href="/login" class="btn">🔄 Try Again</a>
                </div>
            </body>
            </html>
            '''
        
        # Check credentials against database
        try:
            conn = sqlite3.connect('HospitalDB.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Check in employee table
            cursor.execute("SELECT EMP_ID, EMP_NAME FROM employee WHERE EMP_ID=? AND SAL=?", 
                          (username, password))
            emp_result = cursor.fetchone()
            conn.close()
            
            # Check admin credentials
            admin_login = (username == 'admin' and password == 'admin123')
            
            if emp_result or admin_login:
                user_name = emp_result['EMP_NAME'] if emp_result else "Administrator"
                # Set session (simplified)
                return redirect(url_for('main_menu'))
            else:
                return error_page("Invalid Credentials", "The username or password you entered is incorrect.<br>Please check your credentials and try again.")
                
        except Exception as e:
            return error_page("Database Error", f"An error occurred: {str(e)}<br>Please try again later.")
    
    return login_page()

def error_page(title, message):
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
            }}
            .error-container {{
                max-width: 500px;
                width: 100%;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
                text-align: center;
            }}
            .error-icon {{ font-size: 80px; margin-bottom: 20px; }}
            h2 {{ color: #e74c3c; font-size: 28px; font-weight: 600; margin-bottom: 15px; }}
            p {{ color: #7f8c8d; font-size: 16px; margin-bottom: 30px; line-height: 1.6; }}
            .btn {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; padding: 14px 30px; text-decoration: none; border-radius: 8px;
                display: inline-block; font-size: 16px; font-weight: 600;
                transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }}
            .btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4); }}
        </style>
    </head>
    <body>
        <div class="error-container">
            <div class="error-icon">❌</div>
            <h2>{title}</h2>
            <p>{message}</p>
            <a href="/login" class="btn">🔐 Back to Login</a>
        </div>
    </body>
    </html>
    '''

def login_page():
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                position: relative;
                overflow: hidden;
            }
            body::before {
                content: '';
                position: absolute;
                top: -50%;
                right: -50%;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                animation: pulse 4s ease-in-out infinite;
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 0.5; }
                50% { transform: scale(1.1); opacity: 0.8; }
            }
            .login-container {
                display: flex;
                max-width: 900px;
                width: 100%;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
                position: relative;
                z-index: 1;
            }
            .image-section {
                flex: 1;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 40px;
                color: white;
                position: relative;
                overflow: hidden;
            }
            .image-section::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2"/></svg>');
                background-size: 100px 100px;
                opacity: 0.3;
            }
            .hospital-icon {
                font-size: 80px;
                margin-bottom: 20px;
                animation: bounce 2s ease-in-out infinite;
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
            .image-section h2 {
                font-size: 28px;
                font-weight: 600;
                text-align: center;
                margin-bottom: 15px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }
            .image-section p {
                font-size: 14px;
                text-align: center;
                opacity: 0.9;
                line-height: 1.6;
            }
            .features-list {
                margin-top: 30px;
                list-style: none;
            }
            .features-list li {
                margin: 10px 0;
                padding: 8px 15px;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                font-size: 13px;
                backdrop-filter: blur(10px);
            }
            .form-section {
                flex: 1;
                padding: 50px 40px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            .form-header {
                text-align: center;
                margin-bottom: 30px;
            }
            .form-header h1 {
                color: #2c3e50;
                font-size: 32px;
                font-weight: 600;
                margin-bottom: 10px;
            }
            .form-header p {
                color: #7f8c8d;
                font-size: 14px;
            }
            .form-group {
                margin-bottom: 25px;
                position: relative;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
                color: #2c3e50;
                font-size: 14px;
            }
            .form-group input {
                width: 100%;
                padding: 12px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                transition: all 0.3s ease;
                font-family: 'Poppins', sans-serif;
            }
            .form-group input:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            .btn-login {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 14px 30px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                width: 100%;
                transition: all 0.3s ease;
                font-family: 'Poppins', sans-serif;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            .btn-login:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            .btn-login:active {
                transform: translateY(0);
            }
            .credentials-info {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                font-size: 12px;
                border-left: 4px solid #667eea;
            }
            .credentials-info strong {
                color: #667eea;
                display: block;
                margin-bottom: 8px;
            }
            .credentials-info span {
                display: block;
                color: #555;
                margin: 5px 0;
            }
            .divider {
                height: 1px;
                background: linear-gradient(to right, transparent, #e0e0e0, transparent);
                margin: 20px 0;
            }
            @media (max-width: 768px) {
                .login-container {
                    flex-direction: column;
                }
                .image-section {
                    padding: 30px 20px;
                }
                .form-section {
                    padding: 40px 30px;
                }
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="image-section">
                <div class="hospital-icon">🏥</div>
                <h2>Welcome to<br>Hospital Management System</h2>
                <p>Your comprehensive healthcare management solution</p>
                <ul class="features-list">
                    <li>✓ Patient Registration & Records</li>
                    <li>✓ Room Allocation Management</li>
                    <li>✓ Employee Management</li>
                    <li>✓ Appointment Scheduling</li>
                    <li>✓ Billing & Invoicing</li>
                </ul>
            </div>
            <div class="form-section">
                <div class="form-header">
                    <h1>Welcome Back!</h1>
                    <p>Please enter your credentials to login</p>
                </div>
                <form method="POST">
                    <div class="form-group">
                        <label for="username">👤 Username or Email</label>
                        <input type="text" id="username" name="username" placeholder="Enter your username" required autocomplete="username" autofocus>
                    </div>
                    <div class="form-group">
                        <label for="password">🔒 Password</label>
                        <input type="password" id="password" name="password" placeholder="Enter your password" required autocomplete="current-password">
                    </div>
                    <button type="submit" class="btn-login">LOGIN →</button>
                </form>
                <div style="margin-top: 25px; text-align: center; color: #999; font-size: 13px;">
                    <p>🔐 Secure Login | Hospital Management System</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

def nurse_page():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nurse Management - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
                padding: 20px;
            }
            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                border-radius: 15px;
                padding: 20px 30px;
                margin-bottom: 30px;
            }
            .header-content {
                max-width: 1400px;
                margin: 0 auto;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .logo-section {
                display: flex;
                align-items: center;
                gap: 20px;
            }
            .hospital-logo {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 30px;
                color: white;
            }
            h1 { color: #2c3e50; font-size: 28px; }
            .back-btn {
                background-color: #3498db;
                color: white;
                padding: 12px 25px;
                text-decoration: none;
                border-radius: 8px;
                transition: all 0.3s;
            }
            .back-btn:hover { background-color: #2980b9; transform: translateY(-2px); }
            .container { max-width: 1400px; margin: 0 auto; }
            .form-card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 20px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            }
            .form-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                color: #2c3e50;
                font-weight: 600;
                margin-bottom: 8px;
                font-size: 14px;
            }
            input, select {
                width: 100%;
                padding: 12px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                transition: border-color 0.3s;
            }
            input:focus, select:focus {
                outline: none;
                border-color: #ff6b6b;
            }
            .button-group {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                margin-top: 20px;
            }
            .btn {
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            }
            .btn-save {
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                color: white;
            }
            .btn-save:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(17, 153, 142, 0.4); }
            .btn-update { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; }
            .btn-delete { background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%); color: white; }
            .btn-search { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
            .btn-exit { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .btn:hover { transform: translateY(-2px); }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">💉</div>
                    <div>
                        <h1>Nurse Management System</h1>
                        <p style="color: #7f8c8d;">Manage Nursing Staff Efficiently</p>
                    </div>
                </div>
                <a href="/" class="back-btn">
                    <i class="fas fa-arrow-left"></i>
                    Back to Dashboard
                </a>
            </div>
        </div>

        <div class="container">
            <div class="form-card">
                <h2 style="margin-bottom: 20px; color: #ff6b6b;">💉 Nurse Information</h2>
                <form id="nurseForm">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="nurseId">🆔 Nurse ID *</label>
                            <input type="text" id="nurseId" placeholder="Enter unique ID" required>
                        </div>
                        <div class="form-group">
                            <label for="nurseName">👤 Nurse Name *</label>
                            <input type="text" id="nurseName" placeholder="Full name" required>
                        </div>
                        <div class="form-group">
                            <label for="department">🏥 Department</label>
                            <select id="department">
                                <option value="">Select Department</option>
                                <option>Emergency</option>
                                <option>ICU</option>
                                <option>General Ward</option>
                                <option>Pediatrics</option>
                                <option>Operation Theater</option>
                                <option>Labor</option>
                                <option>Outpatient</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="shift">⏰ Shift</label>
                            <select id="shift">
                                <option value="">Select Shift</option>
                                <option>Morning (6AM-2PM)</option>
                                <option>Afternoon (2PM-10PM)</option>
                                <option>Night (10PM-6AM)</option>
                                <option>12 Hours</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="phone">📞 Phone Number</label>
                            <input type="tel" id="phone" placeholder="Contact number">
                        </div>
                        <div class="form-group">
                            <label for="email">📧 Email</label>
                            <input type="email" id="email" placeholder="Email address">
                        </div>
                        <div class="form-group">
                            <label for="experience">💼 Experience (Years)</label>
                            <input type="number" id="experience" placeholder="Years of experience">
                        </div>
                        <div class="form-group">
                            <label for="specialization">🎯 Specialization</label>
                            <input type="text" id="specialization" placeholder="Area of specialization">
                        </div>
                    </div>
                    <div class="button-group">
                        <button type="submit" class="btn btn-save"><i class="fas fa-save"></i> Save Nurse</button>
                        <button type="button" class="btn btn-update"><i class="fas fa-edit"></i> Update</button>
                        <button type="button" class="btn btn-delete"><i class="fas fa-trash"></i> Delete</button>
                        <button type="button" class="btn btn-search"><i class="fas fa-search"></i> Search</button>
                        <button type="button" class="btn btn-exit" onclick="window.location.href='/';"><i class="fas fa-sign-out-alt"></i> Exit</button>
                    </div>
                </form>
            </div>
        </div>

        <script>
            document.getElementById('nurseForm').addEventListener('submit', function(e) {
                e.preventDefault();
                alert('Nurse data saved successfully! (Integration with backend database)');
                // Add actual save logic here
            });
        </script>
    </body>
    </html>
    '''

def view_nurses_page():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>View Nurses - Hospital Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
                padding: 20px;
            }
            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                border-radius: 15px;
                padding: 20px 30px;
                margin-bottom: 30px;
            }
            .header-content {
                max-width: 1400px;
                margin: 0 auto;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .logo-section { display: flex; align-items: center; gap: 20px; }
            .hospital-logo {
                width: 60px; height: 60px;
                background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
                border-radius: 15px;
                display: flex; align-items: center; justify-content: center;
                font-size: 30px; color: white;
            }
            h1 { color: #2c3e50; font-size: 28px; }
            .back-btn {
                background-color: #3498db; color: white;
                padding: 12px 25px; text-decoration: none; border-radius: 8px;
                transition: all 0.3s;
            }
            .back-btn:hover { background-color: #2980b9; transform: translateY(-2px); }
            .container { max-width: 1400px; margin: 0 auto; }
            .stats-card {
                background: white; border-radius: 15px; padding: 25px;
                margin-bottom: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.15);
                display: flex; justify-content: space-between; align-items: center;
            }
            .stat-item { text-align: center; }
            .stat-number { font-size: 36px; font-weight: bold; color: #a18cd1; }
            .stat-label { font-size: 14px; color: #7f8c8d; margin-top: 5px; }
            .table-card {
                background: white; border-radius: 15px; padding: 30px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            }
            table { width: 100%; border-collapse: collapse; }
            thead {
                background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
                color: white;
            }
            th, td { padding: 15px; text-align: left; border-bottom: 1px solid #e0e0e0; }
            th { font-weight: 600; font-size: 14px; }
            td { font-size: 14px; color: #2c3e50; }
            tr:hover { background-color: #f8f9fa; cursor: pointer; }
            .btn {
                padding: 12px 25px; border: none; border-radius: 8px;
                font-size: 14px; font-weight: 600; cursor: pointer;
                transition: all 0.3s; display: inline-flex; align-items: center; gap: 8px;
            }
            .btn-refresh { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; }
            .btn-back { background: #6c757d; color: white; }
            .btn:hover { transform: translateY(-2px); }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="hospital-logo">📋</div>
                    <div>
                        <h1>View All Nurses</h1>
                        <p style="color: #7f8c8d;">Complete Nursing Staff Directory</p>
                    </div>
                </div>
                <a href="/" class="back-btn">
                    <i class="fas fa-arrow-left"></i>
                    Back to Dashboard
                </a>
            </div>
        </div>

        <div class="container">
            <div class="stats-card">
                <div class="stat-item">
                    <div class="stat-number" id="totalNurses">0</div>
                    <div class="stat-label">Total Nurses</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="totalDepts">0</div>
                    <div class="stat-label">Departments</div>
                </div>
                <div>
                    <button class="btn btn-refresh" onclick="loadNurses()">
                        <i class="fas fa-sync-alt"></i> Refresh Data
                    </button>
                </div>
            </div>

            <div class="table-card">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Nurse ID</th>
                            <th>Name</th>
                            <th>Department</th>
                            <th>Shift</th>
                            <th>Phone</th>
                            <th>Email</th>
                            <th>Experience</th>
                            <th>Specialization</th>
                        </tr>
                    </thead>
                    <tbody id="nursesTable">
                        <tr><td colspan="9" style="text-align:center;">Loading...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <script>
            // Sample nurse data (in real app, fetch from backend)
            const nursesData = [
                {id: 'NUR001', name: 'Sarah Johnson', dept: 'Emergency', shift: 'Morning (6AM-2PM)', phone: '555-0101', email: 'sarah.j@hospital.com', exp: '5 years', spec: 'Critical Care'},
                {id: 'NUR002', name: 'Michael Chen', dept: 'ICU', shift: 'Night (10PM-6AM)', phone: '555-0102', email: 'm.chen@hospital.com', exp: '8 years', spec: 'Intensive Care'},
                {id: 'NUR003', name: 'Emily Davis', dept: 'Pediatrics', shift: 'Afternoon (2PM-10PM)', phone: '555-0103', email: 'emily.d@hospital.com', exp: '3 years', spec: 'Pediatric Nursing'}
            ];

            function loadNurses() {
                const tbody = document.getElementById('nursesTable');
                tbody.innerHTML = '';
                
                if (nursesData.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;">No nurses found in database</td></tr>';
                    document.getElementById('totalNurses').textContent = '0';
                    document.getElementById('totalDepts').textContent = '0';
                    return;
                }

                const departments = new Set(nursesData.map(n => n.dept));
                document.getElementById('totalNurses').textContent = nursesData.length;
                document.getElementById('totalDepts').textContent = departments.size;

                nursesData.forEach((nurse, index) => {
                    const row = tbody.insertRow();
                    row.innerHTML = `
                        <td>${index + 1}</td>
                        <td><strong>${nurse.id}</strong></td>
                        <td>${nurse.name}</td>
                        <td>${nurse.dept}</td>
                        <td>${nurse.shift}</td>
                        <td>${nurse.phone}</td>
                        <td>${nurse.email}</td>
                        <td>${nurse.exp}</td>
                        <td>${nurse.spec}</td>
                    `;
                    row.onclick = () => showNurseDetails(nurse);
                });
            }

            function showNurseDetails(nurse) {
                alert(`💉 NURSE DETAILS\n\n` +
                      `🆔 ID: ${nurse.id}\n` +
                      `👤 Name: ${nurse.name}\n` +
                      `🏥 Department: ${nurse.dept}\n` +
                      `⏰ Shift: ${nurse.shift}\n` +
                      `📞 Phone: ${nurse.phone}\n` +
                      `📧 Email: ${nurse.email}\n` +
                      `💼 Experience: ${nurse.exp}\n` +
                      `🎯 Specialization: ${nurse.spec}`);
            }

            // Load on page load
            window.onload = loadNurses;
        </script>
    </body>
    </html>
    '''



@app.route('/')
def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hospital Management System - Login</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .login-container {
            background: white;
            border-radius: 30px;
            box-shadow: 0 30px 90px rgba(0,0,0,0.4);
            overflow: hidden;
            width: 100%;
            max-width: 500px;
            position: relative;
        }
        .header {
            text-align: center;
            padding: 40px 30px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .hospital-icon {
            font-size: 60px;
            margin-bottom: 15px;
        }
        h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .subtitle {
            font-size: 14px;
            opacity: 0.9;
        }
        .role-selector {
            display: flex;
            margin: 30px 30px 20px;
            background: #f5f6fa;
            border-radius: 15px;
            padding: 5px;
        }
        .role-option {
            flex: 1;
            text-align: center;
            padding: 15px 20px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
            font-size: 14px;
        }
        .role-option.active.admin {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .role-option.active.nurse {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            box-shadow: 0 5px 15px rgba(245, 87, 108, 0.4);
        }
        .role-option:not(.active) {
            color: #7f8c8d;
        }
        .role-option:hover:not(.active) {
            background: white;
        }
        .form-container {
            padding: 0 30px 30px;
        }
        .form-group {
            margin-bottom: 25px;
        }
        .form-group label {
            display: block;
            font-size: 12px;
            font-weight: 600;
            color: #2c3e50;
            text-transform: uppercase;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }
        .input-wrapper {
            position: relative;
        }
        .input-icon {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #95a5a6;
            font-size: 16px;
        }
        .form-control {
            width: 100%;
            padding: 15px 15px 15px 45px;
            border: 2px solid #ecf0f1;
            border-radius: 12px;
            font-size: 14px;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s;
        }
        .form-control:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .btn-login {
            width: 100%;
            padding: 16px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: white;
        }
        .btn-admin {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .btn-admin:hover {
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            transform: translateY(-2px);
        }
        .btn-nurse {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        .btn-nurse:hover {
            box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4);
            transform: translateY(-2px);
        }
        .credentials-info {
            margin-top: 25px;
            padding: 20px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        .credentials-info.nurse-mode {
            border-left-color: #f5576c;
        }
        .credentials-title {
            font-size: 11px;
            font-weight: 700;
            color: #2c3e50;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .credential-item {
            font-size: 13px;
            color: #555;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .footer {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            font-size: 12px;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="header">
            <div class="hospital-icon">��</div>
            <h1>HOSPITAL MANAGEMENT</h1>
            <p class="subtitle">Secure Access Portal</p>
        </div>
        
        <div class="role-selector">
            <div class="role-option active admin" id="adminRole" onclick="selectRole('admin')">
                <i class="fas fa-user-tie"></i> Admin
            </div>
            <div class="role-option" id="nurseRole" onclick="selectRole('nurse')">
                <i class="fas fa-user-nurse"></i> Nurse
            </div>
        </div>
        
        <div class="form-container">
            <form id="loginForm" action="/login" method="POST">
                <input type="hidden" id="selectedRole" name="role" value="admin">
                
                <div class="form-group">
                    <label>Username</label>
                    <div class="input-wrapper">
                        <i class="fas fa-user input-icon"></i>
                        <input type="text" id="username" name="username" class="form-control" placeholder="Enter username" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Password</label>
                    <div class="input-wrapper">
                        <i class="fas fa-lock input-icon"></i>
                        <input type="password" id="password" name="password" class="form-control" placeholder="Enter password" required>
                    </div>
                </div>
                
                <button type="submit" class="btn-login btn-admin" id="loginBtn">
                    <i class="fas fa-sign-in-alt"></i> Login as Admin
                </button>
            </form>
            
            <div class="credentials-info" id="credBox">
                <div class="credentials-title">📋 Default Credentials</div>
                <div class="credential-item">
                    <i class="fas fa-user-circle"></i>
                    <span>Username: <strong>admin</strong></span>
                </div>
                <div class="credential-item">
                    <i class="fas fa-key"></i>
                    <span>Password: <strong>admin123</strong></span>
                </div>
            </div>
        </div>
        
        <div class="footer">
            © 2026 Hospital Management System | Integrated Healthcare Platform
        </div>
        
        <div style="padding: 20px; text-align: center; background: white;">
            <p style="color: #7f8c8d; font-size: 13px; margin-bottom: 15px;">Are you a Nurse?</p>
            <a href="/nurse-login" style="display: inline-block; padding: 14px 40px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; text-decoration: none; border-radius: 10px; font-weight: 600; transition: all 0.3s;">
                <i class="fas fa-user-nurse"></i> Go to Nurse Login
            </a>
        </div>
    </div>
    
    <script>
        function selectRole(role) {
            const adminRole = document.getElementById('adminRole');
            const nurseRole = document.getElementById('nurseRole');
            const loginBtn = document.getElementById('loginBtn');
            const credBox = document.getElementById('credBox');
            const selectedRoleInput = document.getElementById('selectedRole');
            const username = document.getElementById('username');
            const password = document.getElementById('password');
            
            if (role === 'admin') {
                adminRole.classList.add('active', 'admin');
                nurseRole.classList.remove('active', 'nurse');
                loginBtn.className = 'btn-login btn-admin';
                loginBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Login as Admin';
                credBox.className = 'credentials-info';
                credBox.innerHTML = \'
                    <div class="credentials-title">📋 Default Credentials</div>
                    <div class="credential-item">
                        <i class="fas fa-user-circle"></i>
                        <span>Username: <strong>admin</strong></span>
                    </div>
                    <div class="credential-item">
                        <i class="fas fa-key"></i>
                        <span>Password: <strong>admin123</strong></span>
                    </div>
                \';
                selectedRoleInput.value = 'admin';
                username.value = '';
                password.value = '';
            } else {
                nurseRole.classList.add('active', 'nurse');
                adminRole.classList.remove('active', 'admin');
                loginBtn.className = 'btn-login btn-nurse';
                loginBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Login as Nurse';
                credBox.className = 'credentials-info nurse-mode';
                credBox.innerHTML = \'
                    <div class="credentials-title">📋 Login Credentials</div>
                    <div class="credential-item">
                        <i class="fas fa-user-circle"></i>
                        <span>Username: <strong>nurse</strong></span>
                    </div>
                    <div class="credential-item">
                        <i class="fas fa-key"></i>
                        <span>Password: <strong>nurse123</strong></span>
                    </div>
                \';
                selectedRoleInput.value = 'nurse';
                username.value = '';
                password.value = '';
            }
        }
    </script>
</body>
</html>"""


# Nurse Portal Web Page
@app.route('/nurse-portal')
def nurse_portal():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nurse Station - Hospital Management System</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Poppins', sans-serif; 
            min-height: 100vh; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1600px; margin: 0 auto; }
        
        /* Header */
        .header { 
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            color: #2c3e50; 
            padding: 30px; 
            border-radius: 25px; 
            margin-bottom: 30px; 
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header-left h1 { 
            font-size: 36px; 
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header-info { 
            display: flex;
            gap: 20px;
            margin-top: 15px;
        }
        .badge {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }
        .live-time {
            background: linear-gradient(135deg, #f093fb, #f5576c);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }
        
        /* Stats Cards */
        .stats-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            gap: 20px;
            transition: all 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        .stat-icon {
            width: 70px;
            height: 70px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            color: white;
        }
        .stat-info h3 { font-size: 28px; margin-bottom: 5px; }
        .stat-info p { color: #7f8c8d; font-size: 14px; }
        
        /* Modules Grid */
        .modules-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 25px;
            margin-bottom: 30px;
        }
        .module-card { 
            background: white; 
            border-radius: 20px; 
            padding: 30px; 
            text-align: center; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: all 0.3s;
            cursor: pointer;
            border-bottom: 5px solid transparent;
            text-decoration: none;
            color: inherit;
            display: block;
            position: relative;
            overflow: hidden;
        }
        .module-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(102,126,234,0.1) 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.3s;
        }
        .module-card:hover::before { opacity: 1; }
        .module-card:hover { 
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        }
        .module-icon { 
            width: 90px; 
            height: 90px; 
            border-radius: 50%; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            margin: 0 auto 20px; 
            font-size: 40px; 
            color: white;
            position: relative;
            z-index: 1;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .module-title { 
            font-size: 22px; 
            font-weight: 700; 
            margin-bottom: 10px; 
            color: #2c3e50;
            position: relative;
            z-index: 1;
        }
        .module-desc { 
            font-size: 14px; 
            color: #7f8c8d;
            position: relative;
            z-index: 1;
        }
        .module-status {
            position: absolute;
            top: 15px;
            right: 15px;
            background: #2ecc71;
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 11px;
            font-weight: 600;
        }
        
        /* Color Themes */
        .patient-module .module-icon { background: linear-gradient(135deg, #3498db, #2980b9); }
        .patient-module { border-bottom-color: #3498db; }
        .medicine-module .module-icon { background: linear-gradient(135deg, #e74c3c, #c0392b); }
        .medicine-module { border-bottom-color: #e74c3c; }
        .schedule-module .module-icon { background: linear-gradient(135deg, #f39c12, #d35400); }
        .schedule-module { border-bottom-color: #f39c12; }
        .ai-module .module-icon { background: linear-gradient(135deg, #2ecc71, #27ae60); }
        .ai-module { border-bottom-color: #2ecc71; }
        .vitals-module .module-icon { background: linear-gradient(135deg, #9b59b6, #8e44ad); }
        .vitals-module { border-bottom-color: #9b59b6; }
        .ward-module .module-icon { background: linear-gradient(135deg, #1abc9c, #16a085); }
        .ward-module { border-bottom-color: #1abc9c; }
        .notes-module .module-icon { background: linear-gradient(135deg, #e67e22, #d35400); }
        .notes-module { border-bottom-color: #e67e22; }
        .emergency-module .module-icon { background: linear-gradient(135deg, #c0392b, #a93226); }
        .emergency-module { border-bottom-color: #c0392b; }
        .blood-module .module-icon { background: linear-gradient(135deg, #ff6b6b, #ee5a6f); }
        .blood-module { border-bottom-color: #ff6b6b; }
        .reports-module .module-icon { background: linear-gradient(135deg, #16a085, #1abc9c); }
        .reports-module { border-bottom-color: #16a085; }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 30px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .back-btn { 
            display: inline-block; 
            padding: 15px 40px; 
            background: linear-gradient(135deg, #95a5a6, #7f8c8d); 
            color: white; 
            text-decoration: none; 
            border-radius: 12px; 
            font-weight: 600; 
            transition: all 0.3s;
            margin: 10px;
        }
        .back-btn:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 10px 30px rgba(149,165,166,0.4); 
        }
        .logout-btn {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-left">
                <h1>💉 NURSE STATION</h1>
                <p style="color: #7f8c8d; font-size: 14px;">Healthcare Professional Dashboard | Emergency Department</p>
                <div class="header-info">
                    <span class="badge"><i class="fas fa-user-nurse"></i> Shift: Morning (6AM-2PM)</span>
                    <span class="badge"><i class="fas fa-hospital"></i> Dept: Emergency & Critical Care</span>
                    <span class="live-time" id="liveTime"><i class="fas fa-clock"></i> --:--:--</span>
                </div>
            </div>
        </div>
        
        <!-- Statistics Row -->
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #3498db, #2980b9);">
                    <i class="fas fa-procedures"></i>
                </div>
                <div class="stat-info">
                    <h3>24/7</h3>
                    <p>Patient Monitoring</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #e74c3c, #c0392b);">
                    <i class="fas fa-pills"></i>
                </div>
                <div class="stat-info">
                    <h3>98%</h3>
                    <p>Medicine Availability</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #2ecc71, #27ae60);">
                    <i class="fas fa-heartbeat"></i>
                </div>
                <div class="stat-info">
                    <h3>150+</h3>
                    <p>Patients Served</p>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #f39c12, #d35400);">
                    <i class="fas fa-user-md"></i>
                </div>
                <div class="stat-info">
                    <h3>12</h3>
                    <p>Medical Staff On-Duty</p>
                </div>
            </div>
        </div>
        
        <!-- Modules Grid -->
        <div class="modules-grid">
            <a href="/view-nurses" class="module-card patient-module">
                <span class="module-status">ACTIVE</span>
                <div class="module-icon"><i class="fas fa-users"></i></div>
                <div class="module-title">👥 Patient Management</div>
                <div class="module-desc">View & manage patient records, admissions, and discharge</div>
            </a>
            
            <a href="/medicine-mgmt" class="module-card medicine-module">
                <span class="module-status">ACTIVE</span>
                <div class="module-icon"><i class="fas fa-pills"></i></div>
                <div class="module-title">💊 Medicine Management</div>
                <div class="module-desc">Track inventory, expiry dates, and stock levels</div>
            </a>
            
            <a href="/doctor-schedule" class="module-card schedule-module">
                <span class="module-status">ACTIVE</span>
                <div class="module-icon"><i class="fas fa-calendar-alt"></i></div>
                <div class="module-title">📅 Doctor Schedule</div>
                <div class="module-desc">View duty roster, timings & on-call doctors</div>
            </a>
            
            <a href="/ai-assistant" class="module-card ai-module">
                <span class="module-status">AI POWERED</span>
                <div class="module-icon"><i class="fas fa-robot"></i></div>
                <div class="module-title">🤖 AI Medical Assistant</div>
                <div class="module-desc">Get instant medical information & drug interactions</div>
            </a>
            
            <a href="/nurse-notice" class="module-card notes-module">
                <span class="module-status">NEW</span>
                <div class="module-icon"><i class="fas fa-clipboard-list"></i></div>
                <div class="module-title">📋 Nurse Notice Board</div>
                <div class="module-desc">Staff announcements, updates & important notices</div>
            </a>
            
            <a href="/ward-mgmt" class="module-card ward-module">
                <span class="module-status">ACTIVE</span>
                <div class="module-icon"><i class="fas fa-procedures"></i></div>
                <div class="module-title">🏥 Ward Management</div>
                <div class="module-desc">Bed allocation, occupancy tracking & room status</div>
            </a>
            
            <a href="/blood-donation" class="module-card blood-module">
                <span class="module-status">URGENT</span>
                <div class="module-icon"><i class="fas fa-tint"></i></div>
                <div class="module-title">🩸 Blood Bank</div>
                <div class="module-desc">Blood availability, donation requests & transfusion</div>
            </a>
            
            <a href="/emergency" class="module-card emergency-module">
                <span class="module-status">24/7</span>
                <div class="module-icon"><i class="fas fa-ambulance"></i></div>
                <div class="module-title">🚨 Emergency Protocol</div>
                <div class="module-desc">Critical response procedures & emergency contacts</div>
            </a>
        </div>
        
        <div class="footer">
            <a href="/nurse-login" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Login</a>
            <a href="/" class="back-btn logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
        </div>
    </div>
    
    <script>
        function updateTime() {
            const now = new Date();
            const timeString = now.toLocaleTimeString('en-US', { hour12: false });
            document.getElementById('liveTime').innerHTML = '<i class="fas fa-clock"></i> ' + timeString;
        }
        setInterval(updateTime, 1000);
        updateTime();
    </script>
</body>
</html>"""

@app.route('/nurse-login')
def nurse_login_page():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nurse Station Login - Hospital Management</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }
        body::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background-image: url('https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=1920&q=80');
            background-size: cover;
            background-position: center;
            opacity: 0.08;
            z-index: 0;
        }
        .login-container {
            background: rgba(255, 255, 255, 0.98);
            border-radius: 30px;
            box-shadow: 0 30px 90px rgba(0,0,0,0.4);
            overflow: hidden;
            width: 100%;
            max-width: 450px;
            position: relative;
            z-index: 1;
        }
        .header {
            text-align: center;
            padding: 45px 30px 30px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            position: relative;
        }
        .header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #ffecd2, #fcb69f);
        }
        .nurse-icon {
            font-size: 70px;
            margin-bottom: 15px;
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .subtitle {
            font-size: 14px;
            opacity: 0.95;
        }
        .form-container {
            padding: 0 30px 30px;
        }
        .form-group {
            margin-bottom: 25px;
        }
        .form-group label {
            display: block;
            font-size: 12px;
            font-weight: 600;
            color: #2c3e50;
            text-transform: uppercase;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }
        .input-wrapper {
            position: relative;
        }
        .input-icon {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #95a5a6;
            font-size: 16px;
            transition: color 0.3s;
        }
        .form-control {
            width: 100%;
            padding: 15px 15px 15px 45px;
            border: 2px solid #ecf0f1;
            border-radius: 12px;
            font-size: 14px;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s;
        }
        .form-control:focus {
            outline: none;
            border-color: #f5576c;
            box-shadow: 0 0 0 3px rgba(245, 87, 108, 0.1);
        }
        .btn-login {
            width: 100%;
            padding: 16px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: white;
            margin-top: 10px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        .btn-login:hover {
            box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4);
            transform: translateY(-2px);
        }
        .info-message {
            margin-top: 20px;
            padding: 18px;
            background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
            border-radius: 12px;
            border-left: 4px solid #f5576c;
            font-size: 13px;
            color: #555;
        }
        .back-link {
            display: block;
            text-align: center;
            margin-top: 20px;
            color: #7f8c8d;
            text-decoration: none;
            font-size: 13px;
        }
        .back-link:hover {
            color: #f5576c;
        }
        .footer {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            font-size: 12px;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="header">
            <div class="nurse-icon">👩‍⚕️</div>
            <h1>NURSE STATION</h1>
            <p class="subtitle">Healthcare Professional Login</p>
        </div>
        
        <div class="form-container">
            <form action="/nurse-auth" method="POST">
                <div class="form-group">
                    <label>Nurse ID</label>
                    <div class="input-wrapper">
                        <i class="fas fa-id-badge input-icon"></i>
                        <input type="text" name="nurse_id" class="form-control" placeholder="Enter your Nurse ID" required autocomplete="off">
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Password</label>
                    <div class="input-wrapper">
                        <i class="fas fa-lock input-icon"></i>
                        <input type="password" name="password" class="form-control" placeholder="Enter your password" required>
                    </div>
                </div>
                
                <button type="submit" class="btn-login">
                    <i class="fas fa-sign-in-alt"></i> Login to Nurse Station
                </button>
            </form>
            
            <div class="info-message">
                <i class="fas fa-info-circle"></i> Use your assigned Nurse ID and password to access the Nurse Station portal.
            </div>
            
            <a href="/" class="back-link">
                <i class="fas fa-arrow-left"></i> Back to Main Login
            </a>
        </div>
        
        <div class="footer">
            © 2026 Hospital Nursing Department | Patient Care Excellence
        </div>
    </div>
</body>
</html>"""

@app.route('/nurse-auth', methods=['POST'])
def nurse_auth():
    nurse_id = request.form.get('nurse_id', '').strip().upper()
    password = request.form.get('password', '').strip()
    
    print(f"NURSE LOGIN ATTEMPT - ID: {nurse_id}")
    
    try:
        conn = sqlite3.connect('HospitalDB.db')
        cursor = conn.cursor()
        
        # Check nurse credentials in database
        cursor.execute("SELECT NURSE_ID, NAME FROM nurse WHERE NURSE_ID=? AND PASSWORD=?", (nurse_id, password))
        nurse = cursor.fetchone()
        
        if nurse:
            print(f"✓ Nurse login successful: {nurse[1]}")
            conn.close()
            return redirect(url_for('nurse_portal'))
        else:
            conn.close()
            print("✗ Login failed")
            
            return """<!DOCTYPE html>
<html>
<head>
    <title>Login Failed</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: Poppins, sans-serif; background: linear-gradient(135deg, #f093fb, #f5576c); display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .error-box { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); text-align: center; max-width: 400px; }
        .error-icon { font-size: 60px; color: #e74c3c; margin-bottom: 20px; }
        h2 { color: #2c3e50; margin-bottom: 10px; }
        p { color: #7f8c8d; margin-bottom: 20px; line-height: 1.6; }
        .btn-back { display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #f093fb, #f5576c); color: white; text-decoration: none; border-radius: 10px; font-weight: 600; transition: all 0.3s; margin: 5px; }
        .btn-back:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4); }
    </style>
</head>
<body>
    <div class="error-box">
        <div class="error-icon">❌</div>
        <h2>Nurse Login Failed!</h2>
        <p>Invalid Nurse ID or password.<br>Please check your credentials and try again.</p>
        <a href="/nurse-login" class="btn-back">← Try Again</a>
        <a href="/" class="btn-back" style="background: linear-gradient(135deg, #667eea, #764ba2);">Main Login</a>
    </div>
</body>
</html>"""
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return f"<h1>Error</h1><p>{str(e)}</p><a href='/nurse-login'>Back to Nurse Login</a>"



# Medicine Management Route
@app.route('/medicine-mgmt')
def medicine_mgmt():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Medicine Management - Nurse Station</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Poppins, sans-serif; min-height: 100vh; background: linear-gradient(135deg, #ecf0f1, #bdc3c7); padding: 20px; }
        .header { background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(231,76,60,0.3); }
        .header h1 { font-size: 36px; margin-bottom: 10px; }
        .content { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 1400px; margin: 0 auto; }
        .back-btn { display: inline-block; padding: 15px 40px; background: linear-gradient(135deg, #95a5a6, #7f8c8d); color: white; text-decoration: none; border-radius: 10px; font-weight: 600; margin-top: 30px; transition: all 0.3s; }
        .back-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(149,165,166,0.4); }
    </style>
</head>
<body>
    <div class="header">
        <h1>💊 MEDICINE MANAGEMENT</h1>
        <p>Pharmacy & Medicine Inventory Control</p>
    </div>
    <div class="content">
        <h2>📦 Medicine Inventory System</h2>
        <p style="margin-top: 20px; color: #7f8c8d;">Manage hospital pharmacy stock, track medicine availability, and monitor expiration dates.</p>
        <div style="margin-top: 30px; padding: 30px; background: #f8f9fa; border-radius: 15px; border-left: 5px solid #e74c3c;">
            <h3><i class="fas fa-info-circle"></i> Features:</h3>
            <ul style="margin-top: 15px; margin-left: 20px; line-height: 2;">
                <li>Add new medicines to inventory</li>
                <li>Track stock levels and expiry dates</li>
                <li>Generate medicine usage reports</li>
                <li>Low stock alerts and notifications</li>
            </ul>
        </div>
    </div>
    <div style="text-align: center;">
        <a href="/nurse-portal" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Nurse Station</a>
    </div>
</body>
</html>"""

# Doctor Schedule Route
@app.route('/doctor-schedule')
def doctor_schedule():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Doctor Schedule - Nurse Station</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Poppins, sans-serif; min-height: 100vh; background: linear-gradient(135deg, #ecf0f1, #bdc3c7); padding: 20px; }
        .header { background: linear-gradient(135deg, #f39c12, #d35400); color: white; padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(243,156,18,0.3); }
        .header h1 { font-size: 36px; margin-bottom: 10px; }
        .content { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 1400px; margin: 0 auto; }
        .back-btn { display: inline-block; padding: 15px 40px; background: linear-gradient(135deg, #95a5a6, #7f8c8d); color: white; text-decoration: none; border-radius: 10px; font-weight: 600; margin-top: 30px; transition: all 0.3s; }
        .back-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(149,165,166,0.4); }
    </style>
</head>
<body>
    <div class="header">
        <h1>📅 DOCTOR SCHEDULE</h1>
        <p>Medical Staff Roster & Duty Timings</p>
    </div>
    <div class="content">
        <h2>👨‍⚕️ Today's Doctor Schedule</h2>
        <p style="margin-top: 20px; color: #7f8c8d;">View doctor rosters, duty timings, and on-call schedules.</p>
        <div style="margin-top: 30px; padding: 30px; background: #f8f9fa; border-radius: 15px; border-left: 5px solid #f39c12;">
            <h3><i class="fas fa-calendar-check"></i> Schedule Information:</h3>
            <ul style="margin-top: 15px; margin-left: 20px; line-height: 2;">
                <li>Morning Shift: 6:00 AM - 2:00 PM</li>
                <li>Evening Shift: 2:00 PM - 10:00 PM</li>
                <li>Night Shift: 10:00 PM - 6:00 AM</li>
                <li>On-call doctors available 24/7</li>
            </ul>
        </div>
    </div>
    <div style="text-align: center;">
        <a href="/nurse-portal" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Nurse Station</a>
    </div>
</body>
</html>"""

# Emergency Route
@app.route('/emergency')
def emergency():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Emergency Protocol - Nurse Station</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Poppins, sans-serif; min-height: 100vh; background: linear-gradient(135deg, #ecf0f1, #bdc3c7); padding: 20px; }
        .header { background: linear-gradient(135deg, #c0392b, #a93226); color: white; padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(192,57,43,0.3); animation: pulse-bg 2s ease-in-out infinite; }
        @keyframes pulse-bg { 0%, 100% { opacity: 1; } 50% { opacity: 0.85; } }
        .header h1 { font-size: 36px; margin-bottom: 10px; }
        .content { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 1400px; margin: 0 auto; }
        .back-btn { display: inline-block; padding: 15px 40px; background: linear-gradient(135deg, #95a5a6, #7f8c8d); color: white; text-decoration: none; border-radius: 10px; font-weight: 600; margin-top: 30px; transition: all 0.3s; }
        .back-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(149,165,166,0.4); }
        .emergency-box { background: linear-gradient(135deg, #ffebee, #ffcdd2); padding: 30px; border-radius: 15px; border-left: 5px solid #c0392b; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚨 EMERGENCY PROTOCOL</h1>
        <p>Critical Response Procedures</p>
    </div>
    <div class="content">
        <h2>⚠️ Emergency Response Guide</h2>
        <p style="margin-top: 20px; color: #7f8c8d;">Quick reference for emergency situations and critical care protocols.</p>
        <div class="emergency-box">
            <h3><i class="fas fa-phone-alt"></i> Emergency Contacts:</h3>
            <ul style="margin-top: 15px; margin-left: 20px; line-height: 2.5; font-size: 16px;">
                <li><strong>Code Blue (Cardiac Arrest):</strong> Dial 911 internally</li>
                <li><strong>Trauma Team:</strong> Extension 100</li>
                <li><strong>ICU Emergency:</strong> Extension 200</li>
                <li><strong>Blood Bank:</strong> Extension 300</li>
            </ul>
        </div>
    </div>
    <div style="text-align: center;">
        <a href="/nurse-portal" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Nurse Station</a>
    </div>
</body>
</html>"""

# Ward Management Route
@app.route('/ward-mgmt')
def ward_mgmt():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ward Management - Nurse Station</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Poppins, sans-serif; min-height: 100vh; background: linear-gradient(135deg, #ecf0f1, #bdc3c7); padding: 20px; }
        .header { background: linear-gradient(135deg, #1abc9c, #16a085); color: white; padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(26,188,156,0.3); }
        .header h1 { font-size: 36px; margin-bottom: 10px; }
        .content { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 1400px; margin: 0 auto; }
        .back-btn { display: inline-block; padding: 15px 40px; background: linear-gradient(135deg, #95a5a6, #7f8c8d); color: white; text-decoration: none; border-radius: 10px; font-weight: 600; margin-top: 30px; transition: all 0.3s; }
        .back-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(149,165,166,0.4); }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 WARD MANAGEMENT</h1>
        <p>Patient Ward & Bed Allocation</p>
    </div>
    <div class="content">
        <h2>🛏️ Ward & Bed Status</h2>
        <p style="margin-top: 20px; color: #7f8c8d;">Monitor bed occupancy, patient admissions, and ward assignments.</p>
        <div style="margin-top: 30px; padding: 30px; background: #f8f9fa; border-radius: 15px; border-left: 5px solid #1abc9c;">
            <h3><i class="fas fa-procedures"></i> Current Ward Status:</h3>
            <ul style="margin-top: 15px; margin-left: 20px; line-height: 2;">
                <li>Total Beds: 150</li>
                <li>Occupied: 120 (80%)</li>
                <li>Available: 30</li>
                <li>ICU Beds: 20 (18 occupied, 2 available)</li>
            </ul>
        </div>
    </div>
    <div style="text-align: center;">
        <a href="/nurse-portal" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Nurse Station</a>
    </div>
</body>
</html>"""

# Blood Donation Route (NEW)
@app.route('/blood-donation')
def blood_donation():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Blood Donation Request - Nurse Station</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Poppins, sans-serif; min-height: 100vh; background: linear-gradient(135deg, #ecf0f1, #bdc3c7); padding: 20px; }
        .header { background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(231,76,60,0.3); }
        .header h1 { font-size: 36px; margin-bottom: 10px; }
        .content { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 1400px; margin: 0 auto; }
        .back-btn { display: inline-block; padding: 15px 40px; background: linear-gradient(135deg, #95a5a6, #7f8c8d); color: white; text-decoration: none; border-radius: 10px; font-weight: 600; margin-top: 30px; transition: all 0.3s; }
        .back-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(149,165,166,0.4); }
        .blood-icon { font-size: 80px; margin-bottom: 20px; animation: beat 1s ease-in-out infinite; }
        @keyframes beat { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
        .urgent-box { background: linear-gradient(135deg, #ffebee, #ffcdd2); padding: 30px; border-radius: 15px; border-left: 5px solid #e74c3c; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <div class="blood-icon">🩸</div>
        <h1>BLOOD DONATION REQUEST</h1>
        <p>Blood Bank & Transfusion Services</p>
    </div>
    <div class="content">
        <h2>🩸 Blood Bank Status</h2>
        <p style="margin-top: 20px; color: #7f8c8d;">Check blood availability, request blood units, and manage transfusion requirements.</p>
        <div class="urgent-box">
            <h3><i class="fas fa-exclamation-triangle"></i> Urgent Requirements:</h3>
            <ul style="margin-top: 15px; margin-left: 20px; line-height: 2.5; font-size: 16px;">
                <li><strong>O+ Blood:</strong> LOW STOCK - Need 10 units</li>
                <li><strong>AB- Blood:</strong> CRITICAL - Need 5 units</li>
                <li><strong>B+ Blood:</strong> Moderate supply</li>
                <li><strong>A+ Blood:</strong> Adequate supply</li>
            </ul>
        </div>
        <div style="margin-top: 30px; padding: 30px; background: #f8f9fa; border-radius: 15px;">
            <h3><i class="fas fa-clock"></i> Blood Bank Hours:</h3>
            <p style="margin-top: 10px; line-height: 2;">Monday - Sunday: 24 Hours Emergency Service<br>Regular Donations: 9:00 AM - 5:00 PM</p>
        </div>
    </div>
    <div style="text-align: center;">
        <a href="/nurse-portal" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Nurse Station</a>
    </div>
</body>
</html>"""

# Nurse Notice Board Route
@app.route('/nurse-notice')
def nurse_notice():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Nurse Notice Board - Nurse Station</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Poppins, sans-serif; min-height: 100vh; background: linear-gradient(135deg, #ecf0f1, #bdc3c7); padding: 20px; }
        .header { background: linear-gradient(135deg, #9b59b6, #8e44ad); color: white; padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(155,89,182,0.3); }
        .header h1 { font-size: 36px; margin-bottom: 10px; }
        .content { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 1400px; margin: 0 auto; }
        .back-btn { display: inline-block; padding: 15px 40px; background: linear-gradient(135deg, #95a5a6, #7f8c8d); color: white; text-decoration: none; border-radius: 10px; font-weight: 600; margin-top: 30px; transition: all 0.3s; }
        .back-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(149,165,166,0.4); }
        .notice-item { background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #9b59b6; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 NURSE NOTICE BOARD</h1>
        <p>Staff Announcements & Updates</p>
    </div>
    <div class="content">
        <h2>📢 Latest Notices</h2>
        <div style="margin-top: 30px;">
            <div class="notice-item">
                <h3><i class="fas fa-bullhorn"></i> Staff Meeting - March 30, 2024</h3>
                <p style="color: #7f8c8d; margin-top: 10px;">Monthly nursing staff meeting in Conference Room A at 2:00 PM</p>
            </div>
            <div class="notice-item">
                <h3><i class="fas fa-graduation-cap"></i> Training Program - April 5, 2024</h3>
                <p style="color: #7f8c8d; margin-top: 10px;">CPR and Emergency Response training for all nursing staff</p>
            </div>
            <div class="notice-item">
                <h3><i class="fas fa-calendar"></i> Holiday Schedule Update</h3>
                <p style="color: #7f8c8d; margin-top: 10px;">Updated roster for upcoming holiday season available at nursing station</p>
            </div>
        </div>
    </div>
    <div style="text-align: center;">
        <a href="/nurse-portal" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Nurse Station</a>
    </div>
</body>
</html>"""



# ============================================
# PATIENT MANAGEMENT - FULL CRUD
# ============================================
@app.route('/view-nurses')
def view_nurses_crud():
    try:
        conn = sqlite3.connect('HospitalDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient ORDER BY P_ID")
        patients = cursor.fetchall()
        conn.close()
        
        patients_html = ""
        for p in patients:
            patients_html += f"""
            <tr>
                <td>{p[0]}</td>
                <td>{p[1]}</td>
                <td>{p[2]}</td>
                <td>{p[3]}</td>
                <td>{p[4]}</td>
                <td>{p[5]}</td>
                <td>
                    <button onclick="editPatient('{p[0]}')" style="padding: 5px 10px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; margin-right: 5px;"><i class="fas fa-edit"></i></button>
                    <button onclick="deletePatient('{p[0]}')" style="padding: 5px 10px; background: #e74c3c; color: white; border: none; border-radius: 5px; cursor: pointer;"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
            """
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Patient Management</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Poppins', sans-serif; min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: rgba(255,255,255,0.95); padding: 30px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .header h1 {{ background: linear-gradient(135deg, #3498db, #2980b9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 36px; }}
        .content {{ background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .btn {{ padding: 12px 25px; border: none; border-radius: 10px; cursor: pointer; font-weight: 600; margin: 10px 5px; transition: all 0.3s; }}
        .btn-primary {{ background: linear-gradient(135deg, #3498db, #2980b9); color: white; }}
        .btn-danger {{ background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; }}
        .btn-success {{ background: linear-gradient(135deg, #2ecc71, #27ae60); color: white; }}
        .btn:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 15px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #ecf0f1; }}
        tr:hover {{ background: #f8f9fa; }}
        .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; }}
        .modal-content {{ background: white; max-width: 600px; margin: 50px auto; padding: 30px; border-radius: 20px; }}
        .form-group {{ margin-bottom: 20px; }}
        .form-group label {{ display: block; margin-bottom: 8px; font-weight: 600; }}
        .form-group input, .form-group select, .form-group textarea {{ width: 100%; padding: 12px; border: 2px solid #ecf0f1; border-radius: 10px; font-family: 'Poppins', sans-serif; }}
        .close {{ float: right; font-size: 28px; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-users"></i> Patient Management</h1>
            <p style="color: #7f8c8d; margin-top: 10px;">View, Add, Edit, and Delete Patient Records</p>
        </div>
        <div class="content">
            <button class="btn btn-primary" onclick="openAddModal()"><i class="fas fa-plus"></i> Add New Patient</button>
            <a href="/nurse-portal" class="btn btn-success"><i class="fas fa-arrow-left"></i> Back to Nurse Station</a>
            
            <table>
                <thead>
                    <tr>
                        <th>Patient ID</th>
                        <th>Name</th>
                        <th>Age</th>
                        <th>Gender</th>
                        <th>Blood Group</th>
                        <th>Disease</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {patients_html}
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- Add/Edit Patient Modal -->
    <div id="patientModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2 id="modalTitle" style="margin-bottom: 20px; color: #2c3e50;">Add New Patient</h2>
            <form id="patientForm" method="POST" action="/patient-action">
                <input type="hidden" id="editMode" name="editMode" value="false">
                <input type="hidden" id="editId" name="editId" value="">
                
                <div class="form-group">
                    <label>Patient ID</label>
                    <input type="text" id="p_id" name="p_id" required placeholder="Enter Patient ID">
                </div>
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" id="p_name" name="p_name" required placeholder="Enter patient name">
                </div>
                <div class="form-group">
                    <label>Age</label>
                    <input type="number" id="p_age" name="p_age" required placeholder="Enter age">
                </div>
                <div class="form-group">
                    <label>Gender</label>
                    <select id="p_gender" name="p_gender" required>
                        <option value="">Select Gender</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Blood Group</label>
                    <select id="p_blood" name="p_blood" required>
                        <option value="">Select Blood Group</option>
                        <option value="A+">A+</option>
                        <option value="A-">A-</option>
                        <option value="B+">B+</option>
                        <option value="B-">B-</option>
                        <option value="O+">O+</option>
                        <option value="O-">O-</option>
                        <option value="AB+">AB+</option>
                        <option value="AB-">AB-</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Disease/Medical Condition</label>
                    <textarea id="p_disease" name="p_disease" rows="3" required placeholder="Enter medical condition"></textarea>
                </div>
                
                <button type="submit" class="btn btn-primary" style="width: 100%;"><i class="fas fa-save"></i> Save Patient</button>
            </form>
        </div>
    </div>
    
    <script>
        function openAddModal() {{
            document.getElementById('modalTitle').innerText = 'Add New Patient';
            document.getElementById('patientForm').reset();
            document.getElementById('editMode').value = 'false';
            document.getElementById('patientModal').style.display = 'block';
        }}
        
        function closeModal() {{
            document.getElementById('patientModal').style.display = 'none';
        }}
        
        function editPatient(id) {{
            // Fetch patient data and populate form
            document.getElementById('modalTitle').innerText = 'Edit Patient';
            document.getElementById('editMode').value = 'true';
            document.getElementById('editId').value = id;
            document.getElementById('patientModal').style.display = 'block';
            // In production, you would fetch the data via AJAX
            alert('Edit functionality - Fetch patient: ' + id);
        }}
        
        function deletePatient(id) {{
            if (confirm('Are you sure you want to delete patient ' + id + '?')) {{
                window.location.href = '/patient-delete/' + id;
            }}
        }}
        
        window.onclick = function(event) {{
            if (event.target == document.getElementById('patientModal')) {{
                closeModal();
            }}
        }}
    </script>
</body>
</html>"""
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

@app.route('/patient-action', methods=['POST'])
def patient_action():
    try:
        edit_mode = request.form.get('editMode', 'false')
        p_id = request.form.get('p_id')
        p_name = request.form.get('p_name')
        p_age = request.form.get('p_age')
        p_gender = request.form.get('p_gender')
        p_blood = request.form.get('p_blood')
        p_disease = request.form.get('p_disease')
        
        conn = sqlite3.connect('HospitalDB.db')
        cursor = conn.cursor()
        
        if edit_mode == 'true':
            edit_id = request.form.get('editId')
            cursor.execute("""UPDATE patient SET P_NAME=?, P_AGE=?, P_GENDER=?, P_BLOODGRP=?, P_DISEASE=? 
                             WHERE P_ID=?""", (p_name, p_age, p_gender, p_blood, p_disease, edit_id))
            conn.commit()
            conn.close()
            return f"<script>alert('Patient updated successfully!'); window.location.href='/view-nurses';</script>"
        else:
            cursor.execute("""INSERT INTO patient (P_ID, P_NAME, P_AGE, P_GENDER, P_BLOODGRP, P_DISEASE) 
                             VALUES (?, ?, ?, ?, ?, ?)""", (p_id, p_name, p_age, p_gender, p_blood, p_disease))
            conn.commit()
            conn.close()
            return f"<script>alert('Patient added successfully!'); window.location.href='/view-nurses';</script>"
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

@app.route('/patient-delete/<p_id>')
def patient_delete(p_id):
    try:
        conn = sqlite3.connect('HospitalDB.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patient WHERE P_ID=?", (p_id,))
        conn.commit()
        conn.close()
        return f"<script>alert('Patient deleted successfully!'); window.location.href='/view-nurses';</script>"
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5002)

# Admin Dashboard Route

@app.route('/login', methods=['POST'])
def login():
    role = request.form.get('role', 'admin')
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    print(f"LOGIN ATTEMPT - Role: {role}, Username: {username}")
    
    try:
        conn = sqlite3.connect('HospitalDB.db')
        cursor = conn.cursor()
        
        success = False
        
        if role == 'admin':
            # First check default admin
            if username == 'admin' and password == 'admin123':
                print("✓ Admin login successful (default)")
                conn.close()
                return redirect(url_for('menu'))
            
            # Check employee table
            cursor.execute("SELECT EMP_ID, EMP_NAME FROM employee WHERE EMP_ID=? AND SAL=?", (username, password))
            emp = cursor.fetchone()
            if emp:
                print(f"✓ Employee login successful: {emp[1]}")
                conn.close()
                return redirect(url_for('menu'))
                
        elif role == 'nurse':
            # First check default nurse
            if username == 'nurse' and password == 'nurse123':
                print("✓ Nurse login successful (default)")
                conn.close()
                return redirect(url_for('nurse_portal'))
            
            # Check nurse table with password
            cursor.execute("SELECT NURSE_ID, NAME FROM nurse WHERE NURSE_ID=? AND PASSWORD=?", (username, password))
            nurse = cursor.fetchone()
            if nurse:
                print(f"✓ Nurse login successful: {nurse[1]}")
                conn.close()
                return redirect(url_for('nurse_portal'))
            
            # Also try phone number as password
            cursor.execute("SELECT NURSE_ID, NAME FROM nurse WHERE NURSE_ID=? AND PHONE=?", (username, password))
            nurse = cursor.fetchone()
            if nurse:
                print(f"✓ Nurse login successful (phone): {nurse[1]}")
                conn.close()
                return redirect(url_for('nurse_portal'))
        
        conn.close()
        print("✗ Login failed")
        
        # Login failed - show error
        return """<!DOCTYPE html>
<html>
<head>
    <title>Login Failed</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: Poppins, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .error-box { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); text-align: center; max-width: 400px; }
        .error-icon { font-size: 60px; color: #e74c3c; margin-bottom: 20px; }
        h2 { color: #2c3e50; margin-bottom: 10px; }
        p { color: #7f8c8d; margin-bottom: 20px; line-height: 1.6; }
        .btn-back { display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; text-decoration: none; border-radius: 10px; font-weight: 600; transition: all 0.3s; }
        .btn-back:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4); }
    </style>
</head>
<body>
    <div class="error-box">
        <div class="error-icon">❌</div>
        <h2>Login Failed!</h2>
        <p>Invalid username or password.<br>Please check your credentials and try again.</p>
        <a href="/" class="btn-back">← Back to Login</a>
    </div>
</body>
</html>"""
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return f"<h1>Error</h1><p>{str(e)}</p><a href='/'>Back to Login</a>"

@app.route('/admin-dashboard', methods=['POST'])
def admin_dashboard():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    if username == 'admin' and password == 'admin123':
        return redirect(url_for('menu'))
    else:
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login Failed</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }
                .error-box {
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    text-align: center;
                }
                .error-icon {
                    font-size: 60px;
                    color: #e74c3c;
                    margin-bottom: 20px;
                }
                h2 { color: #2c3e50; margin-bottom: 10px; }
                p { color: #7f8c8d; margin-bottom: 20px; }
                .btn-back {
                    display: inline-block;
                    padding: 12px 30px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 10px;
                    font-weight: 600;
                    transition: all 0.3s;
                }
                .btn-back:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
                }
            </style>
        </head>
        <body>
            <div class="error-box">
                <div class="error-icon">❌</div>
                <h2>Login Failed!</h2>
                <p>Invalid username or password.</p>
                <a href="/" class="btn-back">← Back to Login</a>
            </div>
        </body>
        </html>
        '''
    return redirect(url_for('menu'))

# Nurse Dashboard Route
@app.route('/nurse-dashboard', methods=['POST'])
def nurse_dashboard():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    if username == 'nurse' and password == 'nurse123':
        return redirect(url_for('nurse_portal'))
    else:
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login Failed</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }
                .error-box {
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    text-align: center;
                }
                .error-icon {
                    font-size: 60px;
                    color: #e74c3c;
                    margin-bottom: 20px;
                }
                h2 { color: #2c3e50; margin-bottom: 10px; }
                p { color: #7f8c8d; margin-bottom: 20px; }
                .btn-back {
                    display: inline-block;
                    padding: 12px 30px;
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 10px;
                    font-weight: 600;
                    transition: all 0.3s;
                }
                .btn-back:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 30px rgba(240, 147, 251, 0.4);
                }
            </style>
        </head>
        <body>
            <div class="error-box">
                <div class="error-icon">❌</div>
                <h2>Login Failed!</h2>
                <p>Invalid username or password.</p>
                <a href="/" class="btn-back">← Back to Login</a>
            </div>
        </body>
        </html>
        '''
