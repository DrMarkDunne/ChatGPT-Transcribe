import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import os
import asyncio
from src.meeting_generator import MeetingGenerator

class TestMeetingGenerator(unittest.TestCase):
    def setUp(self):
        self.api_key = "test-api-key"
        # Patch the OpenAI clients to avoid actual calls
        self.patcher_openai = patch('src.meeting_generator.OpenAI')
        self.patcher_async_openai = patch('src.meeting_generator.AsyncOpenAI')
        self.MockOpenAI = self.patcher_openai.start()
        self.MockAsyncOpenAI = self.patcher_async_openai.start()

        # Setup mocks
        self.mock_client = self.MockOpenAI.return_value
        self.mock_aclient = self.MockAsyncOpenAI.return_value

        self.generator = MeetingGenerator(api_key=self.api_key)

    def tearDown(self):
        self.patcher_openai.stop()
        self.patcher_async_openai.stop()

    def test_transcribe(self):
        # Mock the audio transcription response
        mock_response = MagicMock()
        mock_response.text = "This is a transcribed text."
        self.mock_client.audio.transcriptions.create.return_value = mock_response

        with patch("builtins.open", unittest.mock.mock_open(read_data=b"audio data")):
            result = self.generator.transcribe("dummy_audio.m4a")
            self.assertEqual(result, "This is a transcribed text.")
            self.mock_client.audio.transcriptions.create.assert_called_once()

    def test_generate_minutes(self):
        # Mock the async chat completion response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Mocked Response"))]

        # We need to mock the async call properly.
        # The code calls await aclient.chat.completions.create(...)
        self.mock_aclient.chat.completions.create = AsyncMock(return_value=mock_response)

        transcription = "This is a meeting about something important."

        # Run the async method
        result = asyncio.run(self.generator.generate_minutes(transcription))

        expected_keys = ['abstract_summary', 'key_points', 'action_items', 'sentiment']
        for key in expected_keys:
            self.assertIn(key, result)
            self.assertEqual(result[key], "Mocked Response")

        # Verify it was called 4 times (once for each section)
        self.assertEqual(self.mock_aclient.chat.completions.create.call_count, 4)

    def test_save_as_docx(self):
        minutes = {
            'abstract_summary': "Summary",
            'key_points': "Points",
            'action_items': "Actions",
            'sentiment': "Sentiment"
        }

        with patch('src.meeting_generator.Document') as MockDocument:
            mock_doc = MockDocument.return_value
            filename = self.generator.save_as_docx(minutes, "test_output.docx")

            self.assertEqual(filename, "test_output.docx")
            mock_doc.add_heading.assert_called()
            mock_doc.add_paragraph.assert_called()
            mock_doc.save.assert_called_with("test_output.docx")

if __name__ == '__main__':
    unittest.main()
