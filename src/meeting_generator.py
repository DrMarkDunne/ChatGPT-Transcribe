import asyncio
import os
from openai import AsyncOpenAI, OpenAI
from docx import Document
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict

load_dotenv()

class MeetingGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API Key is required.")
        self.client = OpenAI(api_key=self.api_key)
        self.aclient = AsyncOpenAI(api_key=self.api_key)

    def transcribe(self, audio_file) -> str:
        """
        Transcribes the audio file using OpenAI's Whisper model.
        Accepts a file-like object or a path string.
        """
        # OpenAI v1 requires a file-like object with a name attribute or a path
        # If it's a file path string, open it.
        # If it's a file-like object (like from Streamlit), use it directly.

        # We need to handle if audio_file is a string path or a file-like object
        try:
            if isinstance(audio_file, str):
                 with open(audio_file, "rb") as f:
                     transcription = self.client.audio.transcriptions.create(
                         model="whisper-1",
                         file=f
                     )
            else:
                # Assume it's a file-like object (e.g. from streamlit uploader)
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
        except Exception as e:
            if "413" in str(e) or "too large" in str(e).lower():
                raise ValueError("The audio file is too large. OpenAI Whisper has a 25MB limit. Please compress or trim the file.") from e
            raise e

        return transcription.text

    async def _extract(self, system_prompt: str, text: str) -> str:
        response = await self.aclient.chat.completions.create(
            model="gpt-4",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content

    async def generate_minutes(self, transcription: str) -> Dict[str, str]:
        prompts = {
            'abstract_summary': "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points.",
            'key_points': "You are a proficient AI with a specialty in distilling information into key points. Based on the following text, identify and list the main points that were discussed or brought up. These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about.",
            'action_items': "You are an AI expert in analyzing conversations and extracting action items. Please review the text and identify any tasks, assignments, or actions that were agreed upon or mentioned as needing to be done. These could be tasks assigned to specific individuals, or general actions that the group has decided to take. Please list these action items clearly and concisely.",
            'sentiment': "As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment of the following text. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible."
        }

        # Create tasks for all prompts
        tasks = [self._extract(prompt, transcription) for prompt in prompts.values()]

        # Run them in parallel
        results = await asyncio.gather(*tasks)

        return dict(zip(prompts.keys(), results))

    def save_as_docx(self, minutes: Dict[str, str], filename: str = None) -> str:
        if not filename:
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            filename = f'meeting_minutes_{timestamp}.docx'

        doc = Document()
        for key, value in minutes.items():
            heading = ' '.join(word.capitalize() for word in key.split('_'))
            doc.add_heading(heading, level=1)
            doc.add_paragraph(value)
            doc.add_paragraph()

        doc.save(filename)
        return filename
