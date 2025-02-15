import streamlit as st
from typing import Optional
from groq import Groq
import time
from datetime import datetime

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

def get_ai_response(prompt: str, model_name: Optional[str] = None) -> str:
    """Get response from Groq API with improved error handling"""
    try:
        # Initialize Groq client with API key from secrets
        client = Groq(api_key=st.secrets["AIMLAPIKEY"])
        
        # Use model from secrets if not specified
        model = model_name or st.secrets.get('AIMLAPIMODEL', 'llama-3.3-70b-versatile')
        
        # Create chat completion
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
            model=model,
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract and return the response
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        error_msg = f"API Error: {str(e)}"
        st.error(error_msg)
        st.error("""
        Common issues:
        1. Check if your API key is correct
        2. Verify your internet connection
        3. Make sure you're using a supported model name
        """)
        return "I apologize, but I'm having trouble connecting to the AI service right now. Please try again in a moment."

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
