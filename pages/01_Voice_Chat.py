import streamlit as st
from utils import configure_page_style, display_message, get_ai_response

def voice_chat_page():
    configure_page_style()
    
    st.title("💬 Chat with AI Companion")
    st.subheader("Your Personal Relationship Advisor")
    
    # Voice personality settings
    with st.expander("Chat Settings"):
        personality = st.selectbox(
            "Choose AI Personality",
            ["Supportive Friend", "Dating Coach", "Relationship Therapist"],
            index=0
        )
    
    # Initialize session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # Display chat history
    for message in st.session_state.chat_messages:
        display_message(
            message["content"],
            is_user=(message["role"] == "user")
        )
    
    # Chat input
    user_input = st.text_input("Share your thoughts or ask for advice...", key="voice_chat_input")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get AI response
        prompt = f"""As a {personality}, respond to: {user_input}
        Be empathetic, supportive, and provide practical advice.
        Use emojis appropriately to make the response engaging."""
        
        with st.spinner("Thinking..."):
            response = get_ai_response(prompt)
            
            if response:
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Force a rerun to show the new messages
                st.rerun()

if __name__ == "__main__":
    voice_chat_page()