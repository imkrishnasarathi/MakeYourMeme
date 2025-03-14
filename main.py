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

def find_best_template(topic, templates):
    best_match = None
    best_score = 0

    for template in templates:
        name = template["name"]
        similarity = difflib.SequenceMatcher(None, topic.lower(), name.lower()).ratio()

        if similarity > best_score:
            best_score = similarity
            best_match = template

    print(f"Best match: {best_match['name']} (Score: {best_score})")

    return best_match["url"] if best_match else templates[0]["url"]

template_url = find_best_template(topic, templates)


def create_meme(template_url, text, output_file="meme.jpg"):
    response = requests.get(template_url)
    img = Image.open(BytesIO(response.content))

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Helvetica.ttc", img.width // 15)  # Scales font size dynamically

    max_width = img.width - 40  # Keep some padding
    wrapped_text = wrap_text(draw, text, font, max_width)

    # Positioning text dynamically
    text_height = sum([draw.textbbox((0, 0), line, font=font)[3] for line in wrapped_text])
    text_x = 20  # Padding from left
    text_y = img.height - text_height - 30  # Bottom of image with padding

    for line in wrapped_text:
        draw.text((text_x, text_y), line, font=font, fill="white", stroke_width=3, stroke_fill="black")
        text_y += draw.textbbox((0, 0), line, font=font)[3]  # Move to next line

    img.save(output_file)
    print(f"Meme saved as {output_file}")

# Run meme creation
create_meme(template_url, caption)
