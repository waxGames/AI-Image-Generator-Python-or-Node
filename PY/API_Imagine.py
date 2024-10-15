import json
import socket
from PIL import Image
import io

# MORE INFORMATIONS http://www.technoai.xyz

def create_image(prompt, api_key):
    host = '37.114.41.55' #DON'T CHANGE IP
    port = 6383 # DON'T CHANGE PORT

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        request = {
            "action": "generate",
            "api": api_key,
            "prompt": prompt
        }

        client_socket.sendall(json.dumps(request).encode())

        response = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk

            if b"<END>" in response:
                json_part, image_part = response.split(b"<END>", 1)
                response_data = json.loads(json_part.decode('utf-8', errors='ignore'))

                if response_data.get("status") == "success":
                    image_filename = "generated_image.png"

                    try:
                        image = Image.open(io.BytesIO(image_part))
                        image.load()

                        width, height = image.size
                        bottom_right_pixel = image.getpixel((width-1, height-1))

                        with open(image_filename, "wb") as image_file:
                            image_file.write(image_part)

                        if bottom_right_pixel == (128, 0, 128):
                            break
                    except OSError:
                        print(f"Pls wait image loading.")

if __name__ == "__main__":
    prompt = "Dog." # YOUR PROMPT
    api_key = "" # YOUR API KEY
    create_image(prompt, api_key)
