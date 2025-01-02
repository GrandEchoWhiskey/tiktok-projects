from PIL import Image

# Function to encode a message into an image
def encode_message(image_path: str, message: str, output_path: str) -> None:
    # Open the image
    img = Image.open(image_path)
    img = img.convert("RGB")  # Ensure the image is in RGB format
    pixels = img.load()

    # Convert the message to binary and add a delimiter
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'  # Delimiter

    # Encode the binary message into the pixels
    binary_index = 0
    for y in range(img.height):
        for x in range(img.width):
            if binary_index < len(binary_message):
                r, g, b = pixels[x, y]
                new_r = (r & ~1) | int(binary_message[binary_index])  # Modify the least significant bit
                binary_index += 1
                pixels[x, y] = (new_r, g, b)

    # Save the encoded image
    img.save(output_path)
    print(f"Message encoded and saved to {output_path}.")

# Function to decode a message from an image
def decode_message(image_path: str) -> str:
    # Open the image
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = img.load()

    # Extract the binary message from the pixels
    binary_message = ""
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1)  # Get the least significant bit
            if binary_message.endswith("1111111111111110"):  # Check for delimiter
                break
        else:
            continue
        break

    # Convert the binary message to text
    binary_message = binary_message[:-16]  # Remove the delimiter
    message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

    return message

# Example usage
if __name__ == "__main__":
    # Encode a message
    encode_message("input_image.png", "This is a secret message!", "encoded_image.png")

    # Decode the message
    decoded_message = decode_message("encoded_image.png")
    print("Decoded Message:", decoded_message)