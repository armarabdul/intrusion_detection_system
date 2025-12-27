Anomaly-Based Network Intrusion Detection System
API-Driven Machine Learning Architecture

 Live Application:
 https://intrusion-detection-system-rghn.onrender.com/

 Overview

This project is a production-ready Network Intrusion Detection System (NIDS) built using unsupervised machine learning techniques.
It detects anomalous network behavior by learning patterns of normal traffic and flagging deviations without relying on predefined attack signatures.

The system is designed to resemble a real SOC (Security Operations Center) dashboard, focusing on:

Interpretability

Auditability

Robust backend design

Real-world deployment readiness

 Key Objectives

Detect network intrusions using unsupervised ML

Avoid dependency on labeled attack data during training

Provide explainable detection results

Maintain secure user access

Enable real-time anomaly analysis

Deploy as a cloud-hosted application

 Machine Learning Approach
Models Used

Isolation Forest

One-Class SVM

Strategy

Trained only on normal traffic

Ensemble-based decision making

Threshold-based anomaly detection

No retraining during inference

Dataset

NSL-KDD Dataset

Normal traffic used for training

Attack traffic used only for evaluation

 Advanced Features
 Explainability Layer

Identifies top features contributing to anomaly detection

Provides human-readable explanations instead of black-box outputs

 Confidence & Severity Scoring

Risk levels: LOW / MEDIUM / HIGH

Confidence score (0–100) based on ensemble agreement

 Multi-Model Agreement

Shows whether:

Both models agree

Partial agreement

No agreement

 Data Drift Awareness

Warns when incoming data deviates significantly from training distribution

 Audit Logging

Logs:

User logins

Failed login attempts

Detection requests

High-risk events

Rate Limiting

Protects inference endpoint from abuse

 Attack Simulation Mode

Allows safe simulation of suspicious traffic for demonstration

 Application Architecture
intrusion_detection_system/
│
├── api/                 # Flask backend & API
├── src/                 # ML pipeline (training & scoring)
├── models/              # Trained ML models (.pkl)
├── dashboard/           # Frontend templates & static files
├── data/                # Dataset (raw & processed)
├── results/             # Detection outputs
├── requirements.txt
├── runtime.txt
└── README.md

 Authentication & Security

User registration & login system

Session-based authentication

Protected detection endpoints

Secure environment variable handling

 Frontend Highlights

Dark-themed, SOC-style dashboard

Mobile-responsive UI

Clean, non-AI-generated design

Timeline-based event view

Detection insights & system notes panels

Custom favicon & branding

 Deployment

Platform: Render

Runtime: Python 3.10

Server: Gunicorn

Database: SQLite (academic use)

ML Libraries: scikit-learn, NumPy, pandas

 How to Use

Open the live application
 https://intrusion-detection-system-rghn.onrender.com/

Register a new user account

Login to the dashboard

Use one of the following:

Load Sample Normal Traffic

Simulate Suspicious Traffic

Or manually enter values

Click Analyze Traffic

View:

Risk level

Confidence score

Explanation

Model agreement

Event timeline

 System Notes & Limitations

Flow-level detection (not packet-level)

Unsupervised learning assumptions apply

Thresholds may require periodic review

SQLite database resets on redeploy (acceptable for academic use)

 Internship Credit

Developed during internship at
Zevello Technologies
 https://zevello.co

 Academic Context

Degree: M.Tech (Computer Science / Related)

Domain: Cybersecurity & Machine Learning

Project Type: Internship / Mini Project / Capstone

Focus: Real-world deployable ML system

 Acknowledgement

Alhamdulillah for the successful completion of this project.
This work reflects continuous learning, patience, and persistence through real-world engineering challenges.

 Contact

For queries, feedback, or collaboration:

GitHub: armarabdul

LinkedIn: (as linked in the application footer)

 If you found this project useful or inspiring, feel free to star the repository.