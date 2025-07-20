Music Player Recommendation System

A web-based music recommendation system that detects facial emotion and suggests songs to uplift or match the user's current mood.
Built using Python, Flask, and OpenCV, it enables seamless playback and personalized playlist management.

Features:

1. Live webcam-based facial emotion detection using OpenCV.

2. CNN model trained on the FER2013 dataset with 85% validation accuracy.

3. Emotion-matched music playlists to enhance user experience.

4. Flask-based backend API to serve music files and metadata.

5. Lightweight and responsive front-end UI.

Getting Started
Follow these steps to set up and run the project on your local machine.

Prerequisites
Ensure you have the following installed:

Python 3.8 or higher

pip (Python package installer)

Installation

1. Clone the Repository
```sh   
git clone "https://github.com/manisai11/music.git"
cd "music"
```

3. Create a Virtual Environment (Recommended)
```sh
python -m venv "venv"
```
4. Activate the Virtual Environment

On Windows:
```sh
.\venv\Scripts\activate
```

On macOS/Linux:
```sh
source "venv/bin/activate"
```
4. Install Dependencies
```sh
pip install -r "requirements.txt"
```
5. Run the Application
```sh
python "app.py"
```
