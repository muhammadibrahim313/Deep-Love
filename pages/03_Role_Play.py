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

def role_play_page():
    configure_page_style()
    
    st.title("🎭 Role Play Practice")
    st.subheader("Practice Your Dating Scenarios")
    
    # Scenarios and personalities
    scenarios = {
        "First Date": {
            "description": "Practice first date conversation and body language",
            "personalities": ["Outgoing and Fun", "Shy and Reserved", "Intellectual", "Adventure Seeker"],
            "context": "You're meeting at a cozy café for a first date"
        },
        "Meeting Parents": {
            "description": "Practice meeting your partner's parents for the first time",
            "personalities": ["Traditional Parents", "Modern Parents", "Protective Parents", "Easy-going Parents"],
            "context": "You're visiting their family home for dinner"
        },
        "Approaching Someone": {
            "description": "Practice approaching someone you're interested in",
            "personalities": ["At a Coffee Shop", "At a Party", "At the Gym", "Through Mutual Friends"],
            "context": "You've noticed them and want to start a conversation"
        },
        "Difficult Conversations": {
            "description": "Practice handling challenging relationship discussions",
            "personalities": ["Setting Boundaries", "Discussing Exclusivity", "Addressing Concerns", "Future Planning"],
            "context": "You need to have an important conversation"
        }
    }
    
    # Voice settings
    with st.expander("Voice Settings"):
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Select Voice Gender", ["Female", "Male", "Neutral"])
        with col2:
            voice = st.selectbox("Select Voice", VOICE_OPTIONS[gender])
    
    # Initialize session states
    if "roleplay_messages" not in st.session_state:
        st.session_state.roleplay_messages = []
    if "recording_enabled" not in st.session_state:
        st.session_state.recording_enabled = True
    if "last_response" not in st.session_state:
        st.session_state.last_response = None
    if "audio_played" not in st.session_state:
        st.session_state.audio_played = False
    if "current_scenario" not in st.session_state:
        st.session_state.current_scenario = None
    
    # Scenario setup
    col1, col2 = st.columns([2, 1])
    
    with col1:
        scenario = st.selectbox(
            "Choose Your Scenario",
            list(scenarios.keys())
        )
        st.markdown(f"*{scenarios[scenario]['description']}*")
        
    with col2:
        personality = st.selectbox(
            "Choose Their Personality",
            scenarios[scenario]["personalities"]
        )
    
    # Reset scenario if changed
    if (scenario, personality) != st.session_state.current_scenario:
        st.session_state.current_scenario = (scenario, personality)
        st.session_state.roleplay_messages = []
        st.session_state.recording_enabled = True
        st.session_state.last_response = None
        st.session_state.audio_played = False
    
    # Display chat history
    for message in st.session_state.roleplay_messages:
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
    if st.session_state.recording_enabled and st.session_state.current_scenario:
        with recorder_container:
            audio_data = mic_recorder(
                key="recorder",
                start_prompt="Click to start the conversation",
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
                        st.session_state.roleplay_messages.append({
                            "role": "user",
                            "content": transcription
                        })
                        
                        # Get AI response
                        prompt = f"""You are role-playing as a person in a {scenario} scenario with a {personality} personality.
                        Context: {scenarios[scenario]['context']}
                        User said: "{transcription}"
                        Respond naturally as that character would. Keep it conversational"""
                        
                        response = get_aiml_response(prompt)
                        
                        # Convert response to speech
                        audio_response = text_to_speech(response, voice)
                        
                        # Add AI response
                        st.session_state.roleplay_messages.append({
                            "role": "assistant",
                            "content": response
                        })
                        
                        # Store audio response for autoplay
                        st.session_state.last_response = audio_response
                        
                        # Force refresh to show new messages and play audio
                        st.rerun()

if __name__ == "__main__":
    role_play_page()