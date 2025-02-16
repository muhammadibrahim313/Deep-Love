import streamlit as st
from streamlit_mic_recorder import mic_recorder
from utils import (
    configure_page_style, 
    display_message, 
    get_aiml_response, 
    transcribe_audio,
    text_to_speech,
    VOICE_OPTIONS
)
import base64

def autoplay_audio(audio_bytes):
    """Convert audio bytes to base64 and create an HTML audio player with autoplay"""
    b64 = base64.b64encode(audio_bytes).decode()
    md = f"""
        <audio autoplay onended="this.parentElement.classList.add('audio-done')" class="stAudio">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    st.markdown(md, unsafe_allow_html=True)

def voice_chat_page():
    configure_page_style()
    
    st.title("🎙️ Voice Chat")
    st.subheader("Talk with your AI Companion")
    
    # Voice settings
    with st.expander("Voice Settings"):
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Select Voice Gender", ["Female", "Male", "Neutral"])
        with col2:
            voice = st.selectbox("Select Voice", VOICE_OPTIONS[gender])
    
    # Initialize session states
    if "voice_messages" not in st.session_state:
        st.session_state.voice_messages = []
    if "recording_enabled" not in st.session_state:
        st.session_state.recording_enabled = True
    if "last_response" not in st.session_state:
        st.session_state.last_response = None
    if "audio_played" not in st.session_state:
        st.session_state.audio_played = False
    
    # Display chat history
    for message in st.session_state.voice_messages:
        display_message(
            message["content"],
            is_user=(message["role"] == "user")
        )
    
    # Create a container for the recorder
    recorder_container = st.empty()
    
    # Play last response if exists
    if st.session_state.last_response and not st.session_state.audio_played:
        autoplay_audio(st.session_state.last_response)
        st.session_state.audio_played = True
        st.session_state.last_response = None
        st.session_state.recording_enabled = True
    
    # Audio recording
    if st.session_state.recording_enabled:
        with recorder_container:
            audio_data = mic_recorder(
                key="recorder",
                start_prompt="Click to start recording",
                stop_prompt="Click to stop recording",
                just_once=True
            )
            
            if audio_data and isinstance(audio_data, dict) and audio_data.get("bytes"):
                # Disable recording while processing
                st.session_state.recording_enabled = False
                st.session_state.audio_played = False
                
                # Show recording status
                with st.spinner("Processing your message..."):
                    # Transcribe audio
                    transcription = transcribe_audio(audio_data["bytes"])
                    
                    if transcription:
                        # Add user message
                        st.session_state.voice_messages.append({
                            "role": "user",
                            "content": transcription
                        })
                        
                        # Get AI response
                        response = get_aiml_response(
                            f"Respond briefly and emotionally to: {transcription}. Keep it concise and natural."
                        )
                        
                        # Convert response to speech
                        audio_response = text_to_speech(response, voice)
                        
                        # Add AI response
                        st.session_state.voice_messages.append({
                            "role": "assistant",
                            "content": response
                        })
                        
                        # Store audio response for autoplay
                        st.session_state.last_response = audio_response
                        
                        # Force refresh to show new messages and play audio
                        st.rerun()

if __name__ == "__main__":
    voice_chat_page()