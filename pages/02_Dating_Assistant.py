import streamlit as st
from utils import configure_page_style, display_message, get_aiml_response

def dating_assistant_page():
    configure_page_style()
    
    st.title("💘 Dating Assistant")
    st.subheader("Your Personal Dating Coach")
    
    # Categories
    categories = {
        "Conversation Starters": [
            "How to start a conversation on dating apps",
            "First date conversation topics",
            "How to keep the conversation flowing",
            "Interesting questions to ask"
        ],
        "Flirting Tips": [
            "How to flirt subtly",
            "Reading body language",
            "Showing interest appropriately",
            "Playful texting ideas"
        ],
        "Date Planning": [
            "Creative date ideas",
            "Planning the perfect first date",
            "Romantic gesture suggestions",
            "Making the date memorable"
        ],
        "Dating Strategy": [
            "Building genuine connections",
            "Handling rejection gracefully",
            "Moving from casual to serious",
            "Setting healthy boundaries"
        ]
    }
    
    # Initialize session state
    if "dating_messages" not in st.session_state:
        st.session_state.dating_messages = []
    
    # Create tabs for different categories
    tabs = st.tabs(list(categories.keys()))
    
    for tab, (category, prompts) in zip(tabs, categories.items()):
        with tab:
            st.markdown(f"### {category}")
            cols = st.columns(2)
            for i, prompt in enumerate(prompts):
                col = cols[i % 2]
                with col:
                    if st.button(f"💭 {prompt}", key=f"{category}_{i}"):
                        # Add user message
                        st.session_state.dating_messages.append({
                            "role": "user",
                            "content": prompt
                        })
                        
                        # Get AI response with specific context
                        with st.spinner("Getting expert advice..."):
                            ai_prompt = f"""As a dating coach, provide specific advice about: {prompt}
                            Keep the response practical, supportive, and include relevant emojis.
                            Focus on actionable tips and positive encouragement."""
                            
                            response = get_aiml_response(ai_prompt)
                            st.session_state.dating_messages.append({
                                "role": "assistant",
                                "content": response
                            })
                        st.rerun()
    
    st.markdown("---")
    st.markdown("### Custom Advice")
    
    # Custom input
    custom_situation = st.text_area(
        "Describe your dating situation or question:",
        placeholder="E.g., I'm nervous about my first date tomorrow..."
    )
    
    if st.button("Get Personalized Advice 💝", type="primary"):
        if custom_situation:
            # Add user message
            st.session_state.dating_messages.append({
                "role": "user",
                "content": custom_situation
            })
            
            # Get AI response
            with st.spinner("Getting your personalized advice..."):
                prompt = f"""As an empathetic dating coach, please provide advice for:
                {custom_situation}
                
                Keep the response:
                1. Supportive and understanding
                2. Practical with specific tips
                3. Positive and encouraging
                4. Include relevant emojis
                5. Focus on actionable steps"""
                
                response = get_aiml_response(prompt)
                st.session_state.dating_messages.append({
                    "role": "assistant",
                    "content": response
                })
            st.rerun()
        else:
            st.warning("Please describe your situation first! 💭")
    
    # Display conversation history
    if st.session_state.dating_messages:
        st.markdown("### Your Advice History")
        for message in st.session_state.dating_messages:
            display_message(
                message["content"],
                is_user=(message["role"] == "user")
            )

if __name__ == "__main__":
    dating_assistant_page()