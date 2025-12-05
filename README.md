# SmartTask Prioritizer 🎯

<div align="center">

![SmartTask Prioritizer](https://img.shields.io/badge/🚀-AI%20Powered-blue?style=for-the-badge)
![Django](https://img.shields.io/badge/Django-4.2.7-green?style=for-the-badge)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)

*A beautiful, intelligent task prioritization web app that helps you focus on what matters most!*

![Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=SmartTask+Prioritizer+Demo)    

</div>

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Smart Analysis** | AI-powered task scoring with 4 different strategies |
| 🎨 **Beautiful UI** | Colorful gradients, animations, and modern design |
| ⚡ **Fast & Responsive** | Real-time analysis with instant results |
| 📱 **Mobile Friendly** | Works perfectly on all devices |
| 🔄 **Multiple Strategies** | Choose from 4 prioritization approaches |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 4.2.7
- Modern web browser

Backend Setup

bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
Frontend Setup

bash
cd frontend
python -m http.server 8080
Open your browser

text
http://localhost:8080
🎯 How to Use
Add Tasks: Enter task title, estimated hours, and importance (1-10)

Choose Strategy: Select from 4 AI-powered approaches

Analyze: Click "Analyze Tasks" to see smart prioritization

Get Suggestions: See sample tasks for inspiration

🧠 Prioritization Strategies
Strategy	Best For	Description
🌟 Smart Balance	General Use	Balanced approach considering all factors
⚡ Fastest Wins	Quick Progress	Prioritizes tasks that can be completed quickly
💎 High Impact	Important Goals	Focuses on high-importance tasks
⏰ Deadline Driven	Time-sensitive	Emphasizes urgent tasks with deadlines
📁 Project Structure
text
smarttask-prioritizer/
├── 📂 backend/
│   ├── 📂 task_analyzer/     # Django project
│   ├── 📂 tasks/            # Task management app
│   ├── 📂 scoring/          # AI algorithms
│   ├── manage.py
│   └── requirements.txt
├── 📂 frontend/
│   ├── index.html          # Main application
│   ├── style.css           # Beautiful styling
│   └── script.js           # Interactive features
└── README.md
🛠️ Technology Stack
Backend:

🐍 Django 4.2.7

🎯 Django REST Framework

🗄️ SQLite Database

Frontend:

⚡ Vanilla JavaScript (ES6+)

🎨 Pure CSS3 with Gradients & Animations

📱 Responsive Design

AI Features:

🤖 Custom scoring algorithms

🧮 Multiple prioritization strategies

📊 Intelligent task analysis
