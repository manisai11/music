import streamlit as st
from deepface import DeepFace
import numpy as np
from PIL import Image
import io
import base64

# Set page config
st.set_page_config(
    page_title="Emotion Based Music Player",
    page_icon="🎵",
    layout="wide"
)

# Streamlit interface
def main():
    st.title("Emotion Based Music Player 🎵")
    st.write("Upload your photo or take a picture to play music based on your emotion!")

    # Sidebar information
    st.sidebar.title("About")
    st.sidebar.write("""
    This app detects your emotion and plays matching music!
    
    How to use:
    1. Upload an image or take a photo
    2. Wait for emotion detection
    3. Enjoy the music that matches your mood!
    """)

    # File upload or camera input
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
        # Convert uploaded file to image
        image = Image.open(image_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Convert PIL Image to numpy array
        img_array = np.array(image)

        with st.spinner('Detecting emotion...'):
            # Analyze emotion using DeepFace
            result = DeepFace.analyze(img_array, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']

            # Display results
            display_results(emotion, result[0]['emotion'])
            
            # Play music based on emotion
            play_music(emotion)

    except Exception as e:
        st.error(f"Error processing image: Please try another image with a clear face view.")
        st.write(f"Detailed error: {str(e)}")

def display_results(emotion, emotions_dict):
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

    # Display detected emotion with emoji
    st.write(f"### Detected Emotion: {emotion} {emoji_dict.get(emotion, '')}")

    # Create emotion probability bars
    st.write("### Emotion Probabilities:")
    for emo, prob in emotions_dict.items():
        col1, col2, col3 = st.columns([1, 6, 1])
        with col1:
            st.write(f"{emoji_dict.get(emo, '')}")
        with col2:
            st.progress(prob/100)
        with col3:
            st.write(f"{prob:.1f}%")

def play_music(emotion):
    # Music mapping
    music_files = {
        'happy': 'happy.mp3',
        'sad': 'sad.mp3',
        'angry': 'angry.mp3',
        'neutral': 'neutral.mp3',
        'surprise': 'surprise.mp3',
        'fear': 'sad.mp3',  # Using sad music for fear
        'disgust': 'angry.mp3'  # Using angry music for disgust
    }

    try:
        if emotion in music_files:
            st.write(f"### Now Playing: {emotion.capitalize()} Music 🎵")
            st.audio(f"music/{music_files[emotion]}")
    except Exception as e:
        st.error(f"Error playing music: {str(e)}")

if __name__ == "__main__":
    main()
