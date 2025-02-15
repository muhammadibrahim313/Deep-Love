import streamlit as st
from utils import configure_page_style, display_message, get_ai_response, get_default_prompts

def main():
    configure_page_style()
    
    st.title("💝 Deep Love AI")
    st.subheader("Your Personal Relationship Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Default prompts
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Quick Questions")
        for prompt in get_default_prompts()[:3]:
            if st.button(prompt):
                st.session_state.messages.append({"role": "user", "content": prompt})
    
    with col2:
        for prompt in get_default_prompts()[3:]:
            if st.button(prompt):
                st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display chat history
    for message in st.session_state.messages:
        display_message(
            message["content"],
            is_user=(message["role"] == "user")
        )
    
    # Chat input
    if prompt := st.chat_input("Share your thoughts or ask for advice..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_message(prompt, is_user=True)
        
        with st.spinner("Thinking..."):
            response = get_ai_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            display_message(response)

if __name__ == "__main__":
    main()