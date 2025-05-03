import streamlit as st
from fer import FER
import numpy as np
from PIL import Image
import base64

# Set page config
st.set_page_config(
    page_title="Emotion Music Player",
    page_icon="🎵",
    layout="wide"
)

# Initialize FER detector
detector = FER(mtcnn=True)

def analyze_emotion(image):
    """Analyze emotion in image using FER"""
    try:
        # Convert image to numpy array if it's not already
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Detect emotions
        emotions = detector.detect_emotions(image)
        if emotions:
            # Get the first face detected
            emotions_dict = emotions[0]['emotions']
            dominant_emotion = max(emotions_dict.items(), key=lambda x: x[1])[0]
            return dominant_emotion, emotions_dict
        return None, None
    except Exception as e:
        st.error(f"Error analyzing emotion: {str(e)}")
        return None, None

def display_results(emotion, emotions_dict):
    """Display emotion detection results"""
    if emotion and emotions_dict:
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

        # Display detected emotion
        st.write(f"### Detected Emotion: {emotion.capitalize()} {emoji_dict.get(emotion, '')}")

        # Display emotion probabilities
        st.write("### Emotion Probabilities:")
        for emo, prob in emotions_dict.items():
            col1, col2, col3 = st.columns([1, 6, 1])
            with col1:
                st.write(f"{emoji_dict.get(emo, '')}")
            with col2:
                st.progress(float(prob))
            with col3:
                st.write(f"{prob:.1f}%")

def play_music(emotion):
    """Play music based on detected emotion"""
    if emotion:
        try:
            st.write(f"### Now Playing: {emotion.capitalize()} Music 🎵")
            st.audio(f"music/{emotion.lower()}.mp3")
        except Exception as e:
            st.error(f"Error playing music: {str(e)}")

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
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            
            # Analyze emotion
            with st.spinner('Analyzing emotion...'):
                emotion, emotions_dict = analyze_emotion(image)
                
                # Display results and play music
                if emotion:
                    display_results(emotion, emotions_dict)
                    play_music(emotion)
                else:
                    st.warning("No face detected in the image. Please try another image.")

    else:
        camera_photo = st.camera_input("Take a photo")
        if camera_photo is not None:
            # Display captured image
            image = Image.open(camera_photo)
            
            # Analyze emotion
            with st.spinner('Analyzing emotion...'):
                emotion, emotions_dict = analyze_emotion(image)
                
                # Display results and play music
                if emotion:
                    display_results(emotion, emotions_dict)
                    play_music(emotion)
                else:
                    st.warning("No face detected in the image. Please try another photo.")

if __name__ == "__main__":
    main()
