import streamlit as st
from utils import (
    configure_page_style,
    display_message,
    get_aiml_response,
    transcribe_audio,
    get_llama_response,
    text_to_speech,
    VOICE_OPTIONS,
    get_default_prompts
)

def test_utils():
    configure_page_style()
    st.title("🧪 Deep Love AI - Utils Testing")

    # Test sections
    st.header("1. AIML API Test")
    with st.expander("Test AIML Response"):
        test_prompt = st.text_input("Enter test prompt:", "Tell me about love")
        if st.button("Test AIML Response"):
            with st.spinner("Getting AIML response..."):
                response = get_aiml_response(test_prompt)
                st.write("Response:", response)

    st.header("2. Groq Whisper Test")
    with st.expander("Test Audio Transcription"):
        st.write("Supported formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm")
        st.write("Max file size: 25 MB")
        audio_file = st.file_uploader("Upload audio file", type=['flac', 'mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'ogg', 'wav', 'webm'])
        if audio_file and st.button("Test Transcription"):
            with st.spinner("Transcribing audio..."):
                if audio_bytes := audio_file.read():
                    transcription = transcribe_audio(audio_bytes)
                    if transcription:
                        st.success("Transcription successful!")
                        st.write("Transcribed text:", transcription)
                    else:
                        st.error("Transcription failed. Please check the error message above.")

    st.header("3. Groq Llama Test")
    with st.expander("Test Llama Response"):
        llama_prompt = st.text_input("Enter test prompt for Llama:", "Give me dating advice")
        if st.button("Test Llama Response"):
            with st.spinner("Getting Llama response..."):
                response = get_llama_response(llama_prompt)
                st.write("Response:", response)

    st.header("4. OpenAI TTS Test")
    with st.expander("Test Text-to-Speech"):
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Select Voice Gender", ["Female", "Male", "Neutral"])
        with col2:
            voice = st.selectbox("Select Voice", VOICE_OPTIONS[gender])
        
        test_text = st.text_input("Enter text for TTS:", "Hello, I'm your relationship advisor!")
        if st.button("Test TTS"):
            with st.spinner("Converting to speech..."):
                audio_content = text_to_speech(test_text, voice)
                if audio_content:
                    st.audio(audio_content)

    st.header("5. UI Components Test")
    with st.expander("Test Message Display"):
        test_message = st.text_input("Enter test message:", "This is a test message!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Test User Message"):
                display_message(test_message, is_user=True)
        with col2:
            if st.button("Test Assistant Message"):
                display_message(test_message, is_user=False)

    st.header("6. Default Prompts Test")
    with st.expander("Test Default Prompts"):
        if st.button("Show Default Prompts"):
            prompts = get_default_prompts()
            for prompt in prompts:
                st.write(prompt)

if __name__ == "__main__":
    test_utils()