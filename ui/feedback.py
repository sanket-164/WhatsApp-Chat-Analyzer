import streamlit as st
from utils.constants import FEEDBACK_FILE_PATH
from utils.update_data import read_feedback, add_feedback

def feedback_page():
    # Streamlit UI
    st.title("📝 Feedback Page")

    st.write("Hey, Sanket here! If you liked or didn't like this website, please share your feedback to help me improve. Thank you!")

    # User input fields
    username = st.text_input("Your name")
    feedback = st.text_area("Your feedback")

    # Submit button
    if st.button("Submit Feedback"):
        if username.strip() and feedback.strip():
            add_feedback(FEEDBACK_FILE_PATH, username.strip(), feedback.strip())
            st.success("✅ Feedback submitted successfully!")
            st.rerun()  # Refresh the page to show updated feedback
        else:
            st.warning("⚠️ Please enter both name and feedback.")

    # Display previous feedback
    st.subheader("📌 Previous Feedbacks:")
    feedbacks = read_feedback(FEEDBACK_FILE_PATH)

    if feedbacks:
        for entry in feedbacks:
            st.write(entry.strip())
    else:
        st.write("No feedback yet. Be the first to share your thoughts! 🎉")