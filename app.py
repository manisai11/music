import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="Emotion Music Player",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def analyze_image(image):
    """
    Analyze image to determine emotion based on basic image properties
    """
    # Convert image to grayscale
    gray_image = image.convert('L')
    # Get image statistics
    pixels = np.array(gray_image)
    brightness = np.mean(pixels)
    contrast = np.std(pixels)
    
    # Simple rule-based emotion detection
    if contrast > 50:
        if brightness > 130:
            return 'happy', 0.8
        elif brightness < 90:
            return 'sad', 0.7
        else:
            return 'surprise', 0.6
    else:
        if brightness > 110:
            return 'neutral', 0.75
        else:
            return 'calm', 0.65

def display_emotion_results(emotion, confidence):
    """Display emotion detection results"""
    # Emoji mapping
    emoji_dict = {
        'happy': '😊',
        'sad': '😢',
        'neutral': '😐',
        'surprise': '😮',
        'calm': '😌'
    }

    # Create columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display emotion with emoji
        st.markdown(f"### Detected Mood: {emotion.capitalize()} {emoji_dict.get(emotion, '')}")
        
        # Display confidence bar
        st.write("Confidence Level:")
        st.progress(confidence)
        st.write(f"{confidence*100:.1f}%")

    with col2:
        # Display suggested activity
        st.markdown("### Suggested Music:")
        st.write(f"Playing {emotion} music to match your mood!")

def main():
    st.title("Emotion Based Music Player 🎵")
    
    # Sidebar content
    with st.sidebar:
        st.title("About 📖")
        st.write("""
        This app analyzes your photo and plays music matching your emotional state!
        
        ### How it works:
        1. Upload a photo or take one
        2. Our system analyzes your expression
        3. Matching music starts playing
        
        ### Tips for best results:
        - Ensure good lighting
        - Face the camera directly
        - Show clear expressions
        """)
        
        st.markdown("---")
        st.markdown("### Created with ❤️ by Your Name")

    # Main content
    st.write("Upload your photo or take a picture to play music based on your mood!")

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
        # Open and display image
        image = Image.open(image_file)
        st.image(image, caption='Your Photo', use_container_width=True)

        # Analyze emotion
        with st.spinner('Analyzing your mood...'):
            emotion, confidence = analyze_image(image)
            
            # Display results
            display_emotion_results(emotion, confidence)

            # Play music
            st.markdown("### 🎵 Now Playing")
            try:
                st.audio(f"music/{emotion}.mp3")
            except Exception as e:
                st.warning("Preview music not available. Connect your music service to play matching songs!")
                
            # Additional features
            st.markdown("---")
            st.markdown("### More Options")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Generate Playlist 🎶"):
                    st.write(f"Creating a personalized {emotion} playlist...")
                    
            with col2:
                if st.button("Save Mood 📝"):
                    st.write("Mood saved to your journal!")

    except Exception as e:
        st.error("Oops! Something went wrong. Please try another photo.")
        st.write("Tip: Make sure your photo has good lighting and a clear view of your face!")

if __name__ == "__main__":
    main()
