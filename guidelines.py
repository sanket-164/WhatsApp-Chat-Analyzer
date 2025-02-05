import streamlit as st

def guidelines_page():
    st.title("Guidelines to Export WhatsApp Chats for Analysis")

    st.header("Step-by-Step Guide 📋")

    st.markdown("""
    1. Open **WhatsApp** on your phone.
    2. Navigate to the **chat** you want to export.
    3. Tap the **three-dot menu** (⋮) in the top-right corner.
    4. Select **More > Export Chat**.
    5. Choose **Without Media** (for faster export).
    6. Select a method to share the file (**Email, Google Drive, Save as File**).
    7. Download the `.txt` file and **upload** it for analysis.
    """)

    st.subheader("Why Export Without Media? 📂")
    st.markdown("""
    - Exporting **without media** makes the file smaller and faster to process.
    - Media files (images, videos) **are not needed** for text-based analysis.
    """)

    st.subheader("Your chats are only analysed and are not stored or used elsewhere. They will be automatically cleared upon refresh or closing the website.")