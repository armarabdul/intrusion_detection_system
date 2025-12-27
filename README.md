# 🚨 Anomaly-Based Network Intrusion Detection System  
### API-Driven Machine Learning Architecture

🔗 **Live Application:**  
👉 https://intrusion-detection-system-rghn.onrender.com/

---

## 📌 Overview

This project is a **production-ready Network Intrusion Detection System (NIDS)** built using **unsupervised machine learning** techniques.  
It detects anomalous network behavior by learning patterns of **normal traffic** and flagging deviations without relying on predefined attack signatures.

The system is designed to resemble a **real SOC (Security Operations Center) dashboard**, focusing on:
- Interpretability
- Auditability
- Robust backend design
- Real-world deployment readiness

---

## 🎯 Key Objectives

- Detect network intrusions using **unsupervised ML**
- Avoid dependency on labeled attack data during training
- Provide **explainable detection results**
- Maintain **secure user access**
- Enable **real-time anomaly analysis**
- Deploy as a **cloud-hosted application**

---

## 🧠 Machine Learning Approach

### Models Used
- Isolation Forest  
- One-Class SVM  

### Strategy
- Trained **only on normal traffic**
- Ensemble-based decision making
- Threshold-based anomaly detection
- No retraining during inference

### Dataset
- **NSL-KDD Dataset**
  - Normal traffic used for training
  - Attack traffic used only for evaluation

---

## 🔍 Advanced Features

- **Explainability Layer** – Feature deviation-based explanations  
- **Confidence & Severity Scoring** – LOW / MEDIUM / HIGH with percentage  
- **Multi-Model Agreement** – Strong / Partial / None  
- **Data Drift Awareness** – Distribution deviation warning  
- **Audit Logging** – Login, detection, and high-risk events  
- **Rate Limiting** – Protects inference endpoint  
- **Attack Simulation Mode** – Safe demo of suspicious traffic  

---

## 🖥️ Application Architecture

```
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
```

---

## 🔐 Authentication & Security

- User registration & login
- Session-based authentication
- Protected detection endpoints
- Secure environment variable handling

---

## 🎨 Frontend Highlights

- Dark-themed SOC-style dashboard  
- Mobile responsive UI  
- Timeline-based event view  
- Detection insights & system notes  
- Custom favicon and branding  

---

## ☁️ Deployment

- **Platform:** Render  
- **Runtime:** Python 3.10  
- **Server:** Gunicorn  
- **Database:** SQLite  
- **ML Stack:** scikit-learn, NumPy, pandas  

---

## 🧪 How to Use

1. Open the live app  
2. Register & login  
3. Load sample traffic or simulate attack  
4. Analyze traffic  
5. Review risk, confidence, explanation, and timeline  

---

## ⚠️ System Notes & Limitations

- Flow-level detection only  
- Unsupervised learning assumptions  
- Thresholds may require periodic tuning  
- SQLite resets on redeploy (academic use)

---

## 🧑‍💻 Internship Credit

Developed during internship at  
**Zevello Technologies**  
🌐 https://zevello.co

---

## 📚 Academic Context

- **Degree:** M.Tech  
- **Domain:** Cybersecurity & Machine Learning  
- **Project Type:** Internship / Capstone  
- **Focus:** Deployable ML system  

---

## 🙏 Acknowledgement

Alhamdulillah for the successful completion of this project.

---

## 📩 Contact

- **GitHub:** armarabdul  
- **LinkedIn:** Linked via application footer  

---

⭐ Star the repository if you found this project useful.
