# FITMIND: Exercise & Stress Tracker

**FITMIND** is a web-based wellness app designed for university students to help manage stress, track physical activity, and form healthy habits. It offers a unified platform for stress logging, guided breathing, reminders, journaling, and exercise tracking.

---

## 1. Key Features

- Log stress using a 1–5 scale with mood emojis and optional notes  
- Track exercise activities and view real-time progress charts  
- Practice guided breathing without needing to log in  
- Write and search timestamped notes  
- Set reminders with sound and pop-up notifications  
- Secure login with session-based data access

---

## 2. Requirements

- Python 3.10 or higher  
- Git  
- Virtual environment tool (`venv`)  
- Flask and supporting libraries  

---

## 3. Getting Started

### 3.1 Clone the Repository

```bash
git clone https://github.com/Group-3D-coursework/FITMIND-APP-MAIN-PROJECT.git
cd FITMIND-APP-MAIN-PROJECT
```

---

### 3.2 Create and Activate Virtual Environment

#### On Windows

```bash
py -m venv venv
.\venv\Scripts\activate
```

#### On macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3.3 Install Dependencies

```bash
pip install flask
pip install flask-login
pip install flask-migrate
pip install flask-wtf
pip install flask-mail
pip install itsdangerous
pip install sqlalchemy
pip install password-strength
```

---

## 4. Running the Application

```bash
python main.py
```

Then open your browser and go to:

```text
http://127.0.0.1:5000/
```

---

## 5. Running Tests

### 5.1 Install Testing Tools

```bash
pip install pytest
pip install Flask-Testing
```

### 5.2 Run the Test Suite

```bash
pytest tests
```

Make sure all test files are placed in the `tests/` directory.

---

## 6. Building the Documentation

The documentation is written using **Sphinx** and hosted on **Read the Docs**.
