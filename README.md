# Intelligent Surveillance Analytics Platform

## Real-time Object Tracking Using OpenCV

An AI-powered real-time surveillance analytics system developed using **Python, OpenCV, YOLOv8, and ByteTrack**. This project demonstrates practical applications of Computer Vision for surveillance, object detection, tracking, and analytics.

---

# Table of Contents

1. Project Overview
2. Demo and Screenshots
3. Features
4. Technology Stack
5. Project Structure
6. Installation
7. Running the Project
8. Development Status
9. Future Scope
10. Author
11. License

---

# 1. Project Overview

The Intelligent Surveillance Analytics Platform detects and tracks multiple objects in real time using a webcam or recorded video. Each detected object is assigned a persistent tracking ID, while all tracking events are stored in a database for later analysis.

The project follows a modular architecture and includes:

- Real-time object detection
- Multi-object tracking
- Database logging
- Event logging
- Analytics dashboard
- Video output generation

---

# 3. Features

## Current Features

- Asynchronous multi-threaded tracking
- Spatially indexed category Re-ID memory
- YOLOv8 Medium object detector
- ByteTrack-based object tracking
- Persistent object IDs
- Smart class exclusion filters
- Premium HUD with deterministic colors
- SQLite database logging
- Event logging
- Interactive Streamlit analytics dashboard

### Dashboard Includes

- Object counter
- Detection timeline
- Category distribution
- Historical tracking analytics

## Planned Features

- Multi-camera support
- CUDA GPU acceleration
- Face recognition
- License plate recognition
- PPE detection
- Crowd analysis
- Email and Telegram alerts
- Cloud deployment
- Docker support

---

# 4. Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Computer Vision | OpenCV |
| Object Detection | YOLOv8 |
| Object Tracking | ByteTrack |
| Dashboard | Streamlit |
| Database | SQLite |
| Data Analysis | Pandas |
| Visualization | Plotly |
| IDE | VS Code |

---

# 5. Project Structure

```text
surveillance-ai-platform/
│
├── config/
├── core/
├── dashboard/
├── database/
├── models/
├── outputs/
├── reports/
├── tests/
├── videos/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# 6. Installation

Clone the repository.

```bash
git clone https://github.com/<your-username>/AI-Surveillance-Analytics-Platform.git
```

Navigate to the project directory.

```bash
cd AI-Surveillance-Analytics-Platform
```

Install the required packages.

```bash
pip install -r requirements.txt
```

---

# 7. Running the Project

## Step 1: Run the Surveillance Tracker

```bash
python main.py
```

The application will:

- Process the sample video located in `videos/sample.mp4`
- Detect and track multiple objects
- Display bounding boxes with tracking IDs
- Save tracking information into `database/tracking.db`
- Generate event logs in `reports/event_log.txt`
- Save the annotated output video to `outputs/tracked_output.mp4`

Press **Q** to exit the application.

---

## Step 2: Run the Analytics Dashboard

```bash
streamlit run dashboard/streamlit_app.py
```

The dashboard provides:

- Live object statistics
- Detection history
- Category distribution
- Interactive visualizations

---

# 8. Current Development Status

| Module | Status |
|---------|--------|
| Object Detection | Completed |
| Object Tracking | Completed |
| FPS Monitoring | Completed |
| Database Integration | Completed |
| Event Logging | Completed |
| Dashboard | Completed |
| Object Counter | Completed |
| Analytics | Completed |

---

# 9. Future Scope

Future enhancements include:

- Multi-camera surveillance
- GPU acceleration
- Face recognition
- Automatic number plate recognition
- PPE detection
- Crowd monitoring
- Alert notification system
- Cloud deployment
- Docker containerization

---

# 10. Author

**parth bhutaiya **

B.Tech Computer Science Engineering (AI & ML)

Adani University

Artificial Intelligence Intern

---

# 11. License

This project is intended for educational and research purposes.
