import streamlit as st
from utils import configure_page_style, get_ai_response
import json

def red_flags_page():
    configure_page_style()
    
    st.title("🚩 Red & Green Flags")
    st.subheader("Relationship Health Check")
    
    # Categories of questions
    categories = {
        "Communication": [
            "How do you handle disagreements?",
            "How often do you have deep conversations?",
            "Do you feel heard and understood?",
            "How do they respond to your emotions?"
        ],
        "Boundaries": [
            "Do they respect your personal space?",
            "How do they handle you saying 'no'?",
            "Do they maintain appropriate boundaries with others?",
            "How do they react to your other relationships?"
        ],
        "Trust": [
            "Are they consistent in their words and actions?",
            "Do they keep their promises?",
            "How transparent are they about their life?",
            "Do you feel secure in the relationship?"
        ],
        "Growth": [
            "Do they support your goals and dreams?",
            "How do they handle feedback?",
            "Are they working on self-improvement?",
            "Do you feel like you can grow together?"
        ]
    }
    
    # Initialize session state
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "analysis" not in st.session_state:
        st.session_state.analysis = None
    
    # Create tabs for different categories
    tabs = st.tabs(list(categories.keys()))
    
    for tab, (category, questions) in zip(tabs, categories.items()):
        with tab:
            st.markdown(f"### {category}")
            for i, question in enumerate(questions):
                key = f"{category}_{i}"
                response = st.radio(
                    question,
                    ["Select an answer...", "🟢 Yes, always", "🟡 Sometimes", "🔴 No, rarely"],
                    key=key
                )
                st.session_state.responses[key] = response
    
    # Custom behavior input
    st.markdown("### Add Specific Behaviors")
    col1, col2 = st.columns(2)
    
    with col1:
        behavior = st.text_area(
            "Describe a behavior you've noticed:",
            placeholder="E.g., They always check their phone during our conversations..."
        )
    
    with col2:
        if behavior:
            if st.button("Analyze This Behavior"):
                prompt = f"""Analyze this relationship behavior as a relationship expert:
                "{behavior}"
                
                Determine if this is a red flag 🚩 or green flag 💚 and explain why.
                Include:
                1. Flag classification
                2. Explanation
                3. Potential impact
                4. Advice for handling it
                
                Format with emojis and clear sections."""
                
                analysis = get_ai_response(prompt)
                st.markdown(analysis)
    
    # Overall analysis
    st.markdown("### Get Your Relationship Health Analysis")
    if st.button("Generate Analysis Report 📊"):
        # Filter out unanswered questions
        valid_responses = {
            k: v for k, v in st.session_state.responses.items()
            if v != "Select an answer..."
        }
        
        if len(valid_responses) < 8:  # Require at least 8 answers
            st.warning("Please answer at least 8 questions for a meaningful analysis.")
        else:
            # Prepare the analysis prompt
            responses_text = json.dumps(valid_responses, indent=2)
            
            prompt = f"""As a relationship expert, analyze these responses to relationship questions:
            {responses_text}
            
            Provide a comprehensive analysis including:
            1. Overall relationship health assessment
            2. Key strengths identified
            3. Areas that need attention
            4. Specific recommendations
            5. Action steps for improvement
            
            Format the response with appropriate emojis and clear sections.
            Be constructive and supportive while being honest about concerns."""
            
            with st.spinner("Analyzing your responses..."):
                st.session_state.analysis = get_ai_response(prompt)
    
    if st.session_state.analysis:
        st.markdown("### Your Relationship Health Report")
        st.markdown(st.session_state.analysis)
        
        # Offer to save the report
        if st.download_button(
            "Download Report 📥",
            st.session_state.analysis,
            file_name="relationship_health_report.txt",
            mime="text/plain"
        ):
            st.success("Report downloaded successfully!")

if __name__ == "__main__":
    red_flags_page()
    