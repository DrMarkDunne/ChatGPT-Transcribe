import streamlit as st
import asyncio
import os
from src.meeting_generator import MeetingGenerator

# Page config
st.set_page_config(
    page_title="Meeting Minutes Generator",
    page_icon="📝",
    layout="wide"
)

# Custom CSS for "beautiful" UI
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main {
        background: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("📝 Meeting Minutes Generator")
st.markdown("Upload your audio file to generate professional meeting minutes using AI.")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    api_key_input = st.text_input("OpenAI API Key (Optional if set in env)", type="password")

    st.markdown("---")
    st.info("This tool uses OpenAI's Whisper for transcription and GPT-4 for analysis.")

# Main content
uploaded_file = st.file_uploader("Choose an audio file", type=['m4a', 'mp3', 'wav', 'mp4'])

if uploaded_file is not None:
    st.audio(uploaded_file)

    if st.button("Generate Minutes"):
        api_key = api_key_input or os.getenv("OPENAI_API_KEY")

        if not api_key:
            st.error("Please provide an OpenAI API Key in the sidebar or environment variables.")
        else:
            try:
                generator = MeetingGenerator(api_key=api_key)

                with st.spinner("Transcribing audio... (this might take a while)"):
                    # Transcribe
                    # Streamlit UploadedFile is a file-like object
                    uploaded_file.seek(0)
                    transcription = generator.transcribe(uploaded_file)
                    st.success("Transcription Complete!")

                with st.expander("Show Transcription"):
                    st.text_area("Transcription", transcription, height=200)

                with st.spinner("Analyzing and Generating Minutes..."):
                    # Run async logic
                    minutes = asyncio.run(generator.generate_minutes(transcription))
                    st.success("Minutes Generated!")

                # Display Results
                tab1, tab2, tab3, tab4 = st.tabs(["Abstract", "Key Points", "Action Items", "Sentiment"])

                with tab1:
                    st.subheader("Abstract Summary")
                    st.write(minutes['abstract_summary'])

                with tab2:
                    st.subheader("Key Points")
                    st.write(minutes['key_points'])

                with tab3:
                    st.subheader("Action Items")
                    st.write(minutes['action_items'])

                with tab4:
                    st.subheader("Sentiment Analysis")
                    st.write(minutes['sentiment'])

                # Save and Download
                docx_file = generator.save_as_docx(minutes)
                with open(docx_file, "rb") as f:
                    st.download_button(
                        label="Download DOCX",
                        data=f,
                        file_name=docx_file,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

                # Cleanup (optional, but good for temp files if we saved any, here we just saved the docx)
                # os.remove(docx_file) # Maybe keep it or let user decide.

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
