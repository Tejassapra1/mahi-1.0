import asyncio
from random import randint
from PIL import Image
import os
from time import sleep
from io import BytesIO
from dotenv import dotenv_values
from huggingface_hub import InferenceClient

# Create the Data directory if it doesn't exist
os.makedirs("Data", exist_ok=True)

# Load API token from .env
env_vars = dotenv_values(".env")
HF_TOKEN = env_vars.get("HuggingFaceAPIKey")

# Initialize InferenceClient with auto provider
client = InferenceClient(token=HF_TOKEN, provider="auto")

# Function to open and display images based on a given prompt
def open_images(prompt):
    folder_path = "Data"
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
    for jpg_file in files:
        image_path = os.path.join(folder_path, f'generated_{jpg_file}')
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")


# Async function to generate images using InferenceClient
async def generate_images(prompt: str):
    for i in range(4):
        try:
            # Generate image using the FLUX.1-dev model
            image = await asyncio.to_thread(
                client.text_to_image,
                prompt=f"{prompt}, quality=4K, sharpness-maximum, Ultra High details, high resolution, seed {randint(0, 1000000)}",
                model="black-forest-labs/FLUX.1-dev"
            )
            filename = os.path.join("Data", f"generated_{prompt.replace(' ', '_')}{i + 1}.jpg")
            image.save(filename)
        except Exception as e:
            print(f"Image generation failed: {e}")


# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)


while True:
    try:
        with open("Frontend/Files/ImageGeneration.data", "r") as f:
            data: str = f.read().strip()

        if "," not in data or not data:
            print("Invalid data format in ImageGeneration.data. Skipping...")
            sleep(1)
            continue

        prompt, status = data.split(",", 1)

        # If the status indicates an image generation request
        if status.strip() == "True":
            print("Generating Images...")
            GenerateImages(prompt=prompt.strip())

            # Reset the status in the file after generating images
            with open("Frontend/Files/ImageGeneration.data", "w") as f:
                f.write("False, False")
                break  # Exit the loop after processing the request
        else:
            sleep(1)  # Wait for 1 second before checking again
    except Exception as e:
        print(f"An error occurred: {e}")
        sleep(1)
