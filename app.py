import streamlit as st
from gtts import gTTS
import os
from io import BytesIO
import tempfile
import time

class TextToSpeechConverter:
    def __init__(self):
        # Dictionary of supported languages with their codes
        self.languages = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Italian": "it",
            "Hindi": "hi",
            "Arabic": "ar"
        }
    
    def convert_text_to_speech(self, text, language_code):
        """
        Convert text to speech using gTTS
        
        Args:
            text (str): The text to convert
            language_code (str): The language code (e.g., 'en' for English)
            
        Returns:
            BytesIO: Audio file in memory
        """
        try:
            # Create a BytesIO buffer to store the audio file
            audio_buffer = BytesIO()
            
            # Create gTTS object
            tts = gTTS(text=text, lang=language_code, slow=False)
            
            # Save the audio to the buffer
            tts.write_to_fp(audio_buffer)
            
            # Seek to the beginning of the buffer
            audio_buffer.seek(0)
            
            return audio_buffer
            
        except Exception as e:
            raise Exception(f"Error generating speech: {str(e)}")

def create_streamlit_interface():
    # Set page configuration
    st.set_page_config(
        page_title="Text to Speech Converter",
        page_icon="🔊",
        layout="wide"
    )
    
    # Initialize the converter
    converter = TextToSpeechConverter()
    
    # Create the main interface
    st.title("🎯 Text to Speech Converter")
    st.write("Convert your text to natural-sounding speech in multiple languages")
    
    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input area
        text_input = st.text_area(
            "Enter your text",
            height=150,
            help="Type or paste the text you want to convert to speech"
        )
        
    with col2:
        # Language selection
        selected_language = st.selectbox(
            "Select Language",
            list(converter.languages.keys()),
            help="Choose the language of your input text"
        )
        
        # Speech speed option
        speed = st.slider(
            "Speech Speed",
            min_value=0.5,
            max_value=1.5,
            value=1.0,
            step=0.1,
            help="Adjust the speed of the generated speech"
        )
    
    # Convert button
    if st.button("Convert to Speech", type="primary"):
        if not text_input.strip():
            st.error("Please enter some text to convert")
            return
            
        try:
            # Show processing message
            with st.spinner("Converting text to speech..."):
                # Get language code
                language_code = converter.languages[selected_language]
                
                # Convert text to speech
                audio_buffer = converter.convert_text_to_speech(text_input, language_code)
                
                # Create success message
                st.success("Conversion successful! 🎉")
                
                # Display audio player
                st.audio(audio_buffer, format='audio/mp3')
                
                # Add download button
                st.download_button(
                    label="Download Audio",
                    data=audio_buffer,
                    file_name=f"speech_{int(time.time())}.mp3",
                    mime="audio/mp3"
                )
                
        except Exception as e:
            st.error(f"Error generating speech: {str(e)}")
            
    # Add usage instructions
    with st.expander("How to Use"):
        st.write("""
        1. Enter or paste your text in the text area
        2. Select the appropriate language for your text
        3. Adjust the speech speed if desired
        4. Click 'Convert to Speech' to generate the audio
        5. Use the audio player to listen to the result
        6. Download the audio file if needed
        """)

if __name__ == "__main__":
    create_streamlit_interface()