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