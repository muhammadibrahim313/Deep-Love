import streamlit as st
from utils import configure_page_style, display_message, get_ai_response

def role_play_page():
    configure_page_style()
    
    st.title("🎭 Role Play Practice")
    st.subheader("Practice Your Dating Scenarios")
    
    # Initialize session state
    if "roleplay_messages" not in st.session_state:
        st.session_state.roleplay_messages = []
        st.session_state.current_scenario = None
    
    # Scenario selection
    scenarios = {
        "First Date": {
            "description": "Practice first date conversation and body language",
            "personalities": ["Outgoing and Fun", "Shy and Reserved", "Intellectual", "Adventure Seeker"]
        },
        "Meeting Parents": {
            "description": "Practice meeting your partner's parents for the first time",
            "personalities": ["Traditional Parents", "Modern Parents", "Protective Parents", "Easy-going Parents"]
        },
        "Approaching Someone": {
            "description": "Practice approaching someone you're interested in",
            "personalities": ["At a Coffee Shop", "At a Party", "At the Gym", "Through Mutual Friends"]
        },
        "Difficult Conversations": {
            "description": "Practice handling challenging relationship discussions",
            "personalities": ["Setting Boundaries", "Discussing Exclusivity", "Addressing Concerns", "Future Planning"]
        }
    }
    
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
    
    # Start new scenario
    if (scenario, personality) != st.session_state.current_scenario:
        if st.button("Start New Scenario 🎬"):
            st.session_state.current_scenario = (scenario, personality)
            st.session_state.roleplay_messages = []
            
            # Initial AI response
            prompt = f"""You are role-playing as a person in a {scenario} scenario with a {personality} personality.
            Start the conversation naturally as that person would. Keep responses conversational and realistic.
            Add some light description of body language or tone in [brackets]."""
            
            response = get_ai_response(prompt)
            if response:
                st.session_state.roleplay_messages.append({
                    "role": "assistant",
                    "content": response
                })
    
    # Chat input
    user_input = st.text_input("Your response:", key="roleplay_input")
    
    if user_input:
        st.session_state.roleplay_messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get AI response
        prompt = f"""Continue the {scenario} role-play as a {personality} personality.
        Respond to: "{user_input}"
        Keep the response natural and add body language cues in [brackets]."""
        
        with st.spinner("AI is responding..."):
            response = get_ai_response(prompt)
            if response:
                st.session_state.roleplay_messages.append({
                    "role": "assistant",
                    "content": response
                })
                st.rerun()
    
    # Display conversation
    st.markdown("### Conversation")
    for msg in st.session_state.roleplay_messages:
        display_message(
            f"{'You' if msg['role'] == 'user' else 'Role-play Partner'}: {msg['content']}",
            is_user=(msg["role"] == "user")
        )
    
    # Tips and feedback
    if st.session_state.roleplay_messages:
        with st.expander("Get Feedback on Your Interaction"):
            if st.button("Request Feedback"):
                conversation = "\n".join([
                    f"{'You' if m['role'] == 'user' else 'Partner'}: {m['content']}"
                    for m in st.session_state.roleplay_messages
                ])
                
                feedback_prompt = f"""As a dating coach, analyze this {scenario} role-play conversation:
                {conversation}
                
                Provide specific feedback on:
                1. Communication style
                2. Response appropriateness
                3. Areas for improvement
                4. What was done well
                
                Keep the feedback constructive and encouraging."""
                
                feedback = get_ai_response(feedback_prompt)
                if feedback:
                    st.markdown(feedback)

if __name__ == "__main__":
    role_play_page()