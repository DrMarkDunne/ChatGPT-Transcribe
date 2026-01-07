# Meeting Minutes Generator

A powerful and beautiful tool to generate professional meeting minutes from audio files using OpenAI's Whisper and GPT-4.

## Features

- **Audio Transcription**: Uses OpenAI's Whisper model to accurately transcribe audio files.
- **Automated Minutes**: Generates Abstract Summary, Key Points, Action Items, and Sentiment Analysis using GPT-4.
- **Fast Processing**: Uses parallel requests for efficient generation.
- **Beautiful UI**: User-friendly interface built with Streamlit.
- **Export to DOCX**: Download the generated minutes as a formatted Word document.

## Prerequisites

- Python 3.8+
- OpenAI API Key

## Installation

1. Clone the repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API Key (optional, can also be entered in the UI):

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

To start the application, run:

```bash
streamlit run app.py
```

Upload your audio file (mp3, m4a, wav, mp4), and click "Generate Minutes".

## Testing

To run the tests:

```bash
python -m unittest tests/test_meeting_generator.py
```
