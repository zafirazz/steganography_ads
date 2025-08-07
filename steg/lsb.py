from PIL import Image
import math

def _int_to_bin(n, width):
    return format(n, f'0{width}b')

def embed_message(image_path: str, data: bytes, output_path: str) -> None:
    # Open image
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size
    n_pixels = width * height

    # Prepare data: 4 bytes for length + data
    data_len = len(data)
    if data_len > (n_pixels * 3 - 32) // 8:
        raise ValueError("Data too large to embed in image.")
    length_bytes = data_len.to_bytes(4, byteorder='big')
    full_data = length_bytes + data
    bits = ''.join(_int_to_bin(byte, 8) for byte in full_data)

    # Embed bits into pixels
    bit_idx = 0
    for y in range(height):
        for x in range(width):
            if bit_idx >= len(bits):
                break
            r, g, b = pixels[x, y]
            rgb = [r, g, b]
            for c in range(3):
                if bit_idx < len(bits):
                    rgb[c] = (rgb[c] & ~1) | int(bits[bit_idx])
                    bit_idx += 1
            pixels[x, y] = tuple(rgb)
        if bit_idx >= len(bits):
            break
    img.save(output_path)


def extract_message(image_path: str) -> bytes:
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size

    # Extract first 32 bits for length
    bits = ''
    bit_idx = 0
    for y in range(height):
        for x in range(width):
            for c in range(3):
                bits += str(pixels[x, y][c] & 1)
                bit_idx += 1
                if bit_idx == 32:
                    break
            if bit_idx == 32:
                break
        if bit_idx == 32:
            break
    data_len = int(bits, 2)
    total_bits = (data_len + 4) * 8

    # Extract all bits
    bits = ''
    bit_idx = 0
    for y in range(height):
        for x in range(width):
            for c in range(3):
                bits += str(pixels[x, y][c] & 1)
                bit_idx += 1
                if bit_idx == total_bits:
                    break
            if bit_idx == total_bits:
                break
        if bit_idx == total_bits:
            break
    # Convert bits to bytes
    data_bytes = bytearray()
    for i in range(0, total_bits, 8):
        byte = bits[i:i+8]
        data_bytes.append(int(byte, 2))
    # Remove the first 4 bytes (length)
    return bytes(data_bytes[4:]) 