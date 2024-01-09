import aiohttp
import os
import requests
import time

from typing import AsyncGenerator

from dailyai.services.ai_services import TTSService


class ElevenLabsTTSService(TTSService):
    def __init__(self):
        super().__init__()

        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID")

    async def run_tts(self, sentence) -> AsyncGenerator[bytes, None]:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
            payload = {"text": sentence, "model_id": "eleven_turbo_v2"}
            querystring = {"output_format": "pcm_16000", "optimize_streaming_latency": 2}
            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json",
            }
            async with session.post(url, json=payload, headers=headers, params=querystring) as r:
                if r.status != 200:
                    self.logger.error(
                        f"audio fetch status code: {r.status}, error: {r.text}"
                    )
                    return

                async for chunk in r.content:
                    if chunk:
                        yield chunk
