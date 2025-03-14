import requests
import ollama
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import difflib

def get_meme_templates():
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url).json()
    if response["success"]:
        return response["data"]["memes"]
    return []

templates = get_meme_templates()

def generate_meme_caption(topic):
    response = ollama.chat(
        model="llama2:7b", 
        messages=[{"role": "user", "content": f"Give me ONE short, witty meme caption (max 10 words) for a meme about {topic}. No explanations, just the caption."}]
    )
    return response['message']['content']

topic = "cat being dramatic"
caption = generate_meme_caption(topic)
print("Generated Caption:", caption)

