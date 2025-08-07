from lsb import embed_message, extract_message
from PIL import Image
import os

def create_sample_image(path, size=(100, 100)):
    img = Image.new('RGB', size, color=(255, 255, 255))
    img.save(path)

if __name__ == "__main__":
    original_img = "sample.png"
    stego_img = "stego.png"
    test_message = b"Hello, this is a hidden message!"

    # Create a sample image if it doesn't exist
    if not os.path.exists(original_img):
        create_sample_image(original_img)

    print("Embedding message...")
    embed_message(original_img, test_message, stego_img)
    print(f"Message embedded into {stego_img}")

    print("Extracting message...")
    extracted = extract_message(stego_img)
    print("Extracted message:", extracted)

    assert extracted == test_message, "Extracted message does not match!"
    print("Test passed!") 