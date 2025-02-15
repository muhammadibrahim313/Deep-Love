import streamlit as st
from utils import configure_page_style, display_message, get_ai_response

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
                        st.session_state.dating_messages.append({
                            "role": "user",
                            "content": f"As a dating coach, please help me with: {prompt}"
                        })
    
    st.markdown("---")
    st.markdown("### Custom Advice")
    
    # Custom input
    custom_situation = st.text_area(
        "Describe your dating situation or question:",
        placeholder="E.g., I'm nervous about my first date tomorrow..."
    )
    
    if st.button("Get Personalized Advice 💝", type="primary"):
        if custom_situation:
            prompt = f"""As an empathetic and supportive dating coach, please provide advice for the following situation: 
            {custom_situation}
            
            Format your response with emojis and make it encouraging and actionable."""
            
            st.session_state.dating_messages.append({
                "role": "user",
                "content": custom_situation
            })
            
            with st.spinner("Getting your personalized advice..."):
                response = get_ai_response(prompt)
                st.session_state.dating_messages.append({
                    "role": "assistant",
                    "content": response
                })
    
    # Display conversation history
    st.markdown("### Your Advice History")
    for message in st.session_state.dating_messages:
        display_message(
            message["content"],
            is_user=(message["role"] == "user")
        )

if __name__ == "__main__":
    dating_assistant_page()