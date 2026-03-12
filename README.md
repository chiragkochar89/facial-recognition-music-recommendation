# 🎵 Facial Recognition Based Music Recommendation System

An AI-powered system that detects **facial emotions in real time** and recommends **music playlists based on the detected mood** using **Deep Learning, Computer Vision, and Spotify API**.

---

# 📌 Project Overview

The **Facial Recognition and Music Recommendation System** integrates facial emotion detection with a music recommendation engine to provide a personalized listening experience.

The system captures facial expressions using a webcam, analyzes them using a deep learning model trained on the **FER2013 dataset**, and recommends suitable music based on the detected emotion.

This allows users to receive **dynamic music recommendations that match their mood in real time.**

---

# ❗ Problem Statement

Traditional music recommendation systems depend on **user listening history or manual selection** and cannot understand the user's **real-time emotional state**.

This project solves that problem by:

* Detecting facial expressions
* Identifying user emotions
* Recommending music that matches the detected mood

This creates a **more personalized and emotionally engaging music experience.**

---

# 🚀 Features

* 🎥 Real-time facial emotion detection
* 🎵 Emotion-based music recommendation
* 🤖 Deep learning model for emotion classification
* 🌐 Flask-based web application
* 🔗 Spotify API integration using Spotipy
* ⚡ Multi-threaded video processing for smooth performance

---

# 🏗 System Architecture

Below is the architecture of the system.

![System Architecture](images/architecture.png)

### Workflow

Webcam Input
⬇
Face Detection (OpenCV Haarcascade)
⬇
Emotion Detection Model (CNN trained on FER2013)
⬇
Emotion Classification
⬇
Spotify API
⬇
Music Recommendation
⬇
Display Results on Web Interface

## System Architecture

![System Architecture](images/architecture.png)
---

# 📷 Demo

### Emotion Detection

![Emotion Detection](images/demo1.png)

### Music Recommendation

![Music Recommendation](images/demo2.png)

---

# 🧠 Emotions Detected

The model can detect the following **7 emotions**:

* Happy
* Sad
* Angry
* Surprise
* Fear
* Disgust
* Neutral

---

# 🛠 Tech Stack

### Programming Language

* Python

### Machine Learning / AI

* TensorFlow
* Keras
* OpenCV

### Web Framework

* Flask

### API Integration

* Spotify API (Spotipy)

### Other Libraries

* NumPy
* Pandas
* Scikit-learn

---

# 📂 Project Structure

```
facial-recognition-music-recommendation
│
├── app.py
├── camera.py
├── train.py
├── utils.py
├── Spotify.py
├── model.h5
├── requirements.txt
├── haarcascade_frontalface_default.xml
│
├── templates
│   └── index.html
│
├── images
│   ├── architecture.png
│   ├── demo1.png
│   └── demo2.png
│
└── README.md
```

---

# 📊 Dataset

The model is trained using the **FER2013 Facial Emotion Recognition Dataset**.

Dataset characteristics:

* 48 × 48 grayscale images
* 7 emotion classes
* Used for training CNN based emotion detection model

---

# ▶️ How to Run the Project

### 1️⃣ Clone the repository

```
git clone https://github.com/yourusername/facial-recognition-music-recommendation.git
```

---

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Configure Spotify API

Open **Spotify.py** and add your Spotify developer credentials.

```
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "YOUR_REDIRECT_URI"
```

Create credentials at:

https://developer.spotify.com/dashboard

---

### 4️⃣ Run the application

```
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

Allow **camera permission** when prompted.

---

# ⚠️ Limitations

* Emotion detection accuracy depends on lighting and camera quality
* Model accuracy may vary for different facial expressions
* Cannot be deployed directly on cloud servers due to webcam dependency

---

# 🔮 Future Improvements

* Improve emotion detection accuracy using advanced deep learning models
* Enable client-side webcam streaming for cloud deployment
* Add direct Spotify music playback
* Implement personalized recommendation learning

---

# 👨‍💻 Contributors

* Chirag Mahavir Kochar
* Sumit Jibhau Bhamare
* Pawan Shivaji Ghule
* Rohan Balasaheb Bornare

---

# 📜 License

This project is developed for **academic and educational purposes**.
