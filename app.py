import streamlit as st
from PIL import Image
import numpy as np
import requests
import json
import io
import base64

# Set page config
st.set_page_config(
    page_title="Emotion Music Player",
    page_icon="🎵",
    layout="wide"
)

# Using Hugging Face API for emotion detection
def detect_emotion(image):
    API_URL = "https://api-inference.huggingface.co/models/dima806/facial_emotions_image_detection"
    headers = {"Authorization": f"Bearer {st.secrets['huggingface_token']}"}
    
    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    try:
        response = requests.post(API_URL, headers=headers, data=img_byte_arr)
        return response.json()
    except Exception as e:
        st.error(f"Error in emotion detection: {str(e)}")
        return None

def map_emotion_to_music(emotion):
    emotion_music_map = {
        'happy': 'happy.mp3',
        'sad': 'sad.mp3',
        'neutral': 'neutral.mp3',
        'angry': 'angry.mp3',
        'surprise': 'surprise.mp3',
        'fear': 'sad.mp3',
        'disgust': 'angry.mp3'
    }
    return emotion_music_map.get(emotion.lower(), 'neutral.mp3')

def display_emotion_results(emotion, confidence):
    # Emoji mapping
    emoji_dict = {
        'happy': '😊',
        'sad': '😢',
        'angry': '😠',
        'neutral': '😐',
        'surprise': '😮',
        'fear': '😨',
        'disgust': '🤢'
    }

    # Display emotion with emoji
    st.write(f"### Detected Emotion: {emotion} {emoji_dict.get(emotion.lower(), '')}")
    
    # Display confidence
    st.write("### Confidence Score:")
    st.progress(confidence)
    st.write(f"{confidence:.1f}%")

def main():
    st.title("Emotion Based Music Player 🎵")
    st.write("Upload your photo or take a picture to play music based on your emotion!")

    # Sidebar
    st.sidebar.title("About")
    st.sidebar.write("""
    This app detects your emotion and plays matching music!
    
    How to use:
    1. Upload an image or take a photo
    2. Wait for emotion detection
    3. Enjoy the music that matches your mood!
    """)

    # Image input options
    option = st.radio("Choose input method:", ["Upload Image", "Take Photo"])

    if option == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
        if uploaded_file is not None:
            process_image(uploaded_file)
    else:
        camera_photo = st.camera_input("Take a photo")
        if camera_photo is not None:
            process_image(camera_photo)

def process_image(image_file):
    try:
        # Display uploaded/captured image
        image = Image.open(image_file)
        st.image(image, caption='Processed Image', use_column_width=True)

        # Detect emotion
        with st.spinner('Analyzing emotion...'):
            result = detect_emotion(image)
            
            if result and isinstance(result, list) and len(result) > 0:
                # Get the emotion with highest confidence
                emotion_data = result[0]
                emotion = emotion_data['label']
                confidence = emotion_data['score'] * 100

                # Display results
                display_emotion_results(emotion, confidence)

                # Play corresponding music
                music_file = map_emotion_to_music(emotion)
                st.write(f"### Now Playing: {emotion.capitalize()} Music 🎵")
                st.audio(f"music/{music_file}")
            else:
                st.warning("No face detected. Please try another image with a clear face view.")

    except Exception as e:
        st.error(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    main()
