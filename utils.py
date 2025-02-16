import streamlit as st
from typing import Optional
from groq import Groq
import openai
import time
from datetime import datetime
import os
import tempfile
import wave

def configure_page_style():
    """Configure the base page styling"""
    st.set_page_config(
        page_title="Deep Love AI",
        page_icon="💝",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
        <style>
        .stApp {
            background-color: #fdf2f8;
        }
        .main {
            background-color: #fdf2f8;
        }
        .stButton button {
            background-color: #ec4899;
            color: white;
            border-radius: 20px;
            padding: 0.5rem 2rem;
            border: none;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .stButton button:hover {
            background-color: #db2777;
            border: none;
        }
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        .stTextInput input {
            border-radius: 15px;
        }
        .styled-message {
            padding: 1rem;
            border-radius: 15px;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .user-message {
            background-color: #fce7f3;
            margin-left: 2rem;
        }
        .assistant-message {
            background-color: #fbcfe8;
            margin-right: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

def display_message(text: str, is_user: bool = False):
    """Display a message with custom styling"""
    message_class = "user-message" if is_user else "assistant-message"
    st.markdown(
        f'<div class="styled-message {message_class}">{text}</div>',
        unsafe_allow_html=True
    )

def get_aiml_response(prompt: str) -> str:
    """Get response from AIML API using OpenAI library"""
    try:
        client = openai.OpenAI(
            api_key=st.secrets["AIMLAPIKEY"],
            base_url=st.secrets["AIMLAPIENDPOINT"]
        )
        
        response = client.chat.completions.create(
            model=st.secrets["AIMLAPIMODEL"],
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and empathetic relationship advisor. Provide warm, supportive responses with appropriate emojis and clear, practical advice."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Get the full response
        full_response = response.choices[0].message.content
        
        # Filter out the thinking process
        if "<think>" in full_response:
            # Split by the last occurrence of </think> to get the actual response
            actual_response = full_response.split("</think>")[-1].strip()
        else:
            actual_response = full_response
            
        #print("Filtered response:", actual_response)  # For debugging
        return actual_response
        
    except Exception as e:
        st.error(f"AIML API Error: {str(e)}")
        return "I'm having trouble connecting to the service. Please try again! 💝"

def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe audio using Groq's Whisper model"""
    try:
        # Initialize Groq client
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_file_path = temp_file.name
        
        print(f"Transcribing audio file: {temp_file_path}")
        
        # Transcribe using Groq
        with open(temp_file_path, 'rb') as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=audio_file,
                response_format="text"
            )
        
        # Clean up temporary file
        os.remove(temp_file_path)
        
        if response:
            print("Transcription successful!")
            return response
        
    except Exception as e:
        st.error(f"Whisper Transcription Error: {str(e)}")
        print(f"Error during transcription: {str(e)}")
        return None

def get_llama_response(prompt: str) -> str:
    """Get response from Groq's Llama model"""
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and empathetic relationship advisor. Provide warm, supportive responses with appropriate emojis and clear, practical advice."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=st.secrets["GROQ_LLAMA_MODEL"],
            temperature=0.7,
            max_tokens=1000
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Llama Model Error: {str(e)}")
        return "I'm having trouble with the Llama model. Please try again! 💝"

def text_to_speech(text: str, voice: str = "nova") -> bytes:
    """Convert text to speech using OpenAI's TTS"""
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice.lower(),
            input=text
        )
        return response.content
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")
        return None

VOICE_OPTIONS = {
    "Female": ["Nova", "Alloy", "Shimmer", "Echo"],
    "Male": ["Onyx", "Fable", "Sage"],
    "Neutral": ["Coral", "Ash"]
}

def get_default_prompts() -> list:
    """Return default conversation prompts"""
    return [
        "💝 Help me plan a romantic date",
        "🎁 I need gift ideas for my partner",
        "💕 Give me some flirting tips",
        "😊 How to start a conversation",
        "🚩 What are some relationship red flags?",
        "💑 How to improve communication in my relationship"
    ]
