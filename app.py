import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import base64
from PIL import Image
import io

# Set page config
st.set_page_config(
    page_title="Emotion Based Music Player",
    page_icon="🎵",
    layout="wide"
)

# Function to play audio HTML
def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

# Dictionary mapping emotions to music files
emotion_music = {
    'happy': 'happy.mp3',
    'sad': 'sad.mp3',
    'neutral': 'neutral.mp3',
    'angry': 'angry.mp3',
    'surprise': 'surprise.mp3'
}

def main():
    st.title("Emotion Based Music Player 🎵")
    st.write("Upload your photo or take a picture to play music based on your emotion!")

    # Sidebar
    st.sidebar.title("About")
    st.sidebar.write("""
    This app detects your emotion from your image and plays matching music!
    
    How it works:
    1. Upload an image or take a photo
    2. The app detects your emotion
    3. Music matching your emotion plays automatically
    """)

    # Main content
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Upload Image or Take Photo")
        # File uploader
        uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
        # Camera input
        camera_photo = st.camera_input("Or take a photo")

    with col2:
        if uploaded_file is not None or camera_photo is not None:
            image_file = uploaded_file if uploaded_file is not None else camera_photo
            
            # Display the uploaded image
            image = Image.open(image_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)

            # Convert PIL Image to numpy array
            image_np = np.array(image)

            try:
                # Analyze emotion
                result = DeepFace.analyze(image_np, actions=['emotion'])
                emotion = result[0]['dominant_emotion']

                # Display results with emoji
                emoji_dict = {
                    'happy': '😊',
                    'sad': '😢',
                    'angry': '😠',
                    'neutral': '😐',
                    'surprise': '😮'
                }

                # Display emotion with emoji
                st.write(f"### Detected Emotion: {emotion} {emoji_dict.get(emotion, '')}")

                # Display emotion probabilities
                st.write("### Emotion Probabilities:")
                emotions = result[0]['emotion']
                for emo, prob in emotions.items():
                    st.progress(prob/100)
                    st.write(f"{emo}: {prob:.2f}%")

                # Play corresponding music
                if emotion in emotion_music:
                    st.write(f"Playing music for {emotion} emotion...")
                    st.audio(f"music/{emotion_music[emotion]}")

            except Exception as e:
                st.error(f"Error in emotion detection: {str(e)}")
                st.write("Please try another image with a clear face view.")

if __name__ == "__main__":
    main()