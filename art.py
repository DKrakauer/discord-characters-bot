import json
import base64
import requests
import io
from PIL import Image, PngImagePlugin


# Submit a POST request to a server.
def submit_post(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))


# Save the given image to a local folder
def save_encoded_image(b64_image: str, output_path: str):
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))


# Easy function to throw a prompt into to make the bot code easier to read
def go_make_art_with_this(prompt: str, output_path: str):
    url = "http://127.0.0.1:7860"
    payload = {
        "prompt": prompt,
        "steps": 25,
        "width": 512,
        "height": 512,
        "restore_faces": True,

    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    print(r)

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save('output.png', pnginfo=pnginfo)

go_make_art_with_this("Dark ranger hunter with long flowing blonde hair, purple black armor, no helmet, large bow, wolf pet companion, and a quiver of arrows on her back.", "test.png")