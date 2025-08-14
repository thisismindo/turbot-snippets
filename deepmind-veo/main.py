import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ.get('GOOGLE_API_KEY'))
filename = 'f-one.mp4'

prompt = """A dynamic, low-angle cinematic shot of a Formula 1 car hurtling around a rain-soaked track.
The car is a blur of motion, with spray kicking up from the tires and a trail of vapor from the rear.
The scene is lit by the glare of track lights reflecting off the wet asphalt, emphasizing the intense speed and the challenging conditions.
The background features a crowd of spectators, their faces a wash of color, blurred by the motion."""

operation = client.models.generate_videos(
    model="veo-3.0-generate-preview",
    prompt=prompt,
)

operation = types.GenerateVideosOperation(name=operation.name)

while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(15)
    operation = client.operations.get(operation)

try:
    generated_video = operation.response.generated_videos[0]

    client.files.download(file=generated_video.video)

    generated_video.video.save(filename)
    print(f"Generated video saved to {filename}")
except AttributeError as e:
    print(e)
