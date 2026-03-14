# 🌿 AgroVision AI — Intelligent Crop Disease Diagnostic System

AgroVision AI is an end-to-end **AI-powered crop health analysis platform** that detects plant diseases from leaf images and provides actionable agricultural recommendations including NPK fertilizer guidance, environmental intelligence, and treatment strategies.

This system combines **Deep Learning, Computer Vision, Environmental Data, and Agricultural Knowledge** to assist farmers and researchers in diagnosing crop diseases quickly and accurately.

---

# 🚀 Features

### 🌱 AI Disease Detection

* Detects crop diseases using a trained **EfficientNet-B0 deep learning model**
* Supports **multiple plant disease classes**
* Provides **AI confidence score**

### 🔬 Explainable AI (Heatmaps)

* Uses **Grad-CAM visualization**
* Highlights infected regions in the leaf image
* Improves model interpretability

### 🌦 Environmental Intelligence

* Fetches **real-time weather data**
* Analyzes:

  * Temperature
  * Humidity
  * Disease spread risk

### 🧪 Smart Fertilizer Recommendation

* Generates **NPK fertilizer suggestions**
* Provides detailed reasoning
* Helps improve soil nutrient balance

### 🌾 Crop Rotation Intelligence

* Suggests optimal **next crop rotation strategy**
* Helps prevent disease recurrence

### 📊 Comprehensive Action Plan

The system generates a **full treatment plan including:**

* Root cause analysis
* Soil health improvement
* Fertilizer schedule
* Disease control strategies
* Irrigation management
* Farm hygiene recommendations

### 📄 Automated AI Report

Generates a downloadable **PDF diagnostic report** containing:

* Disease identification
* Confidence score
* Original leaf image
* AI heatmap visualization
* Environmental intelligence
* Fertilizer and treatment recommendations

---

# 🧠 System Architecture

```
Leaf Image Upload
        │
        ▼
AI Disease Detection Model
(EfficientNet-B0)
        │
        ▼
Heatmap Generation (GradCAM)
        │
        ▼
Environmental Intelligence
(Weather API)
        │
        ▼
NPK Recommendation Engine
        │
        ▼
Crop Rotation Advisor
        │
        ▼
Comprehensive Action Plan
        │
        ▼
PDF Diagnostic Report
```

---

# 🧰 Tech Stack

### AI & Machine Learning

* Python
* PyTorch
* EfficientNet-B0
* Grad-CAM
* OpenCV

### Backend

* FastAPI
* Uvicorn

### Frontend

* Streamlit Dashboard

### Cloud & Database

* Firebase Firestore

### Data & APIs

* Weather API
* Kaggle Plant Disease Dataset

---

# 📂 Project Structure

```
agrovision-ai
│
├── ai_engine
│   ├── disease_detector.py
│   ├── agro_analysis.py
│   ├── npk_recommender.py
│   ├── weather_service.py
│
├── dashboard
│   └── app.py
│
├── models
│   └── crop_disease_model.pth
│
├── services
│   ├── report_generator.py
│
├── data
│
├── temp_uploads
│
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

### 1️⃣ Clone Repository

```
git clone https://github.com/YOUR_USERNAME/agrovision-ai.git
cd agrovision-ai
```

### 2️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate environment:

Windows

```
venv\Scripts\activate
```

Linux / Mac

```
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

# ▶️ Run the System

### Start Backend API

```
uvicorn main:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

### Start Dashboard

```
streamlit run dashboard/app.py
```

Dashboard runs on:

```
http://localhost:8501
```

---

# 📸 Example Output

The system produces:

* Disease Prediction
* AI Confidence Score
* GradCAM Heatmap
* Environmental Intelligence
* NPK Fertilizer Recommendation
* Crop Rotation Plan
* Detailed Treatment Strategy
* Downloadable PDF Report

---

# 🌍 Real World Applications

* Precision Agriculture
* Smart Farming Systems
* Agricultural Advisory Platforms
* Crop Monitoring Systems
* Agricultural AI Research

---

# 🔮 Future Improvements

* Mobile application for farmers
* Drone image integration
* Satellite crop monitoring
* Soil sensor integration
* Yield prediction AI
* Multi-language farmer interface

---

# 👨‍💻 Author

Developed by **sathwik**

AI & Machine Learning Enthusiast
Building intelligent systems for real-world agricultural challenges.

---

# ⭐ Support

If you found this project useful, please ⭐ star the repository on GitHub!
