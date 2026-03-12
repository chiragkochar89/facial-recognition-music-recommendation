# 🎵 Facial Recognition Based Music Recommendation System

A smart web application that detects **facial emotions in real time** and recommends **music playlists based on the detected emotion** using **Deep Learning and Spotify API**.

---

## 📌 Project Overview

This project uses a **Convolutional Neural Network (CNN)** trained on the **FER2013 dataset** to detect facial emotions from a webcam feed.
Once an emotion is detected, the system recommends **music playlists from Spotify** that match the user’s mood.

The application is built using **Python, OpenCV, TensorFlow/Keras, Flask, and Spotipy API**.

---

## 🎯 Key Features

* 🎥 **Real-time facial emotion detection**
* 🎵 **Automatic music recommendation based on mood**
* 📡 **Spotify API integration using Spotipy**
* 🧠 **Deep learning model trained on FER2013 dataset**
* 🌐 **Web interface built with Flask**
* ⚡ **Multithreading for smooth video streaming**

---

## 🧠 Emotions Detected

The model can detect the following **7 emotions**:

* Angry
* Disgust
* Fear
* Happy
* Sad
* Surprise
* Neutral

---

## 🛠️ Tech Stack

**Programming & Frameworks**

* Python
* Flask

**Machine Learning / AI**

* TensorFlow
* Keras
* OpenCV

**API**

* Spotipy (Spotify API Wrapper)

**Testing Interface**

* Tkinter

---

## 📂 Dataset

The model is trained using the **FER2013 dataset**, which is a widely used dataset for facial emotion recognition.

Dataset characteristics:

* 48 × 48 grayscale images
* 7 emotion classes
* Highly imbalanced dataset

Training accuracy achieved: **~66%**

---

## 🧱 Model Architecture

The deep learning model is a **Sequential CNN architecture** consisting of:

* Conv2D layers (32–128 filters, ReLU activation)
* MaxPooling layers (2×2)
* Dropout layers (0.25)
* Dense layers
* Final **Softmax layer for 7-class emotion classification**

**Loss Function:** Categorical Crossentropy
**Optimizer:** Adam
**Metric:** Accuracy

---

## 🖼️ Image Processing & Training

Image preprocessing steps:

* Images resized to **48×48**
* Converted to **grayscale**
* Normalized pixel values
* Batch size: **64**

Training details:

* Epochs: **75**
* Training Time: **~13 hours**
* Accuracy: **~66%**

---

## ⚙️ Project Structure

```
facial-recognition-music-recommendation
│
├── app.py                # Main Flask application
├── camera.py             # Video capture and emotion prediction
├── train.py              # Model training script
├── utils.py              # Utility functions
├── Spotipy.py            # Spotify API integration
├── model.h5              # Trained emotion detection model
├── requirements.txt      # Python dependencies
├── haarcascade_frontalface_default.xml  # Face detection model
└── templates/
    └── index.html        # Web interface
```

---

## ▶️ Running the Application

### 1️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 2️⃣ Configure Spotify API

Open **Spotipy.py** and add your Spotify developer credentials.

```
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "YOUR_REDIRECT_URI"
```

Create credentials at:
https://developer.spotify.com/dashboard

---

### 3️⃣ Run the application

```
python app.py
```

Allow **camera permission** when prompted.

The application will start on:

```
http://127.0.0.1:5000
```

---

## ⚠️ Current Limitations

* The application currently **cannot be deployed directly to cloud servers** because OpenCV accesses the **server-side webcam instead of the client webcam**.
* Model accuracy is moderate (**~66%**) and can be improved with better training.

---

## 🚀 Future Improvements

* Improve model accuracy using **Vision Transformer or improved CNN models**
* Add **direct Spotify song playback**
* Store playlists in a **database**
* Update recommendation playlists automatically
* Enable **client-side video streaming for cloud deployment**

---

## 👨‍💻 Contributors

* **Chirag Kochar**

---

## 📜 License

This project is for **educational and academic purposes**.

---

## ⭐ If you like this project

Give it a **star on GitHub ⭐**
