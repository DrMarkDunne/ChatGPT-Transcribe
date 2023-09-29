# ChatGPT-Transcribe
A simple Python-based tool to transcribe audio files using OpenAI and GPT-4.

## Prerequisites
- An OpenAI account and API key. You can obtain it from the [OpenAI website](https://openai.com/)
- Python 3.x installed
- pip installed

## Required Python Libraries
- openai
- python-dotenv
- python-docx

You can install these using pip:
```bash
pip install openai python-dotenv python-docx
```

## Setup
1. Clone the repository or download the zip file and extract it.
2. Navigate to the project directory.
3. Create a .env file in the project directory and add your OpenAI API key in that file:
```bash
API_KEY=<your OpenAI API key here>
```
4. Install the necessary libraries.

## How to Run
You can run the project with Python:
```bash
python test.py
```
In `test.py`, replace `"Earningscall.wav"` with the path to your audio file.

## Description
This tool transcribes an audio file into text using the OpenAI audio transcription model. It then uses GPT-4 to extract meeting minutes, including the abstract summary, key points, action items, and sentiment analysis of the transcription. The results are saved as a `meeting_minutes.docx` Word file.

Please note that for large audio files, the script breaks the audio file into smaller chunks and transcribes each separately to adhere to OpenAI's API content size limits.

## Limitations
Due to OpenAI's API content size limitations, this tool might not work with large audio files (greater than 25 MB).

## License
This project is licensed under the MIT License.

## Contact
For any issues or suggestions related to this tool, please contact the repository owner.
