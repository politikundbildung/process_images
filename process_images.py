import os
import argparse
from PIL import Image as PILImage
import numpy as np
import doxapy
import img2pdf
from tqdm import tqdm
import io
from wand.image import Image as WandImage

def deskew_image(input_path):
    # Open the image using Wand and apply deskew
    with WandImage(filename=input_path) as img:
        img.deskew(0.8 * img.quantum_range)
        # Convert the deskewed image to a byte array for further processing
        byte_array = np.array(bytearray(img.make_blob(format='png')))
        return PILImage.open(io.BytesIO(byte_array))

def process_image(input_path):
    # Deskew the image first
    deskewed_image = deskew_image(input_path)

    # Convert the deskewed image to grayscale numpy array
    grayscale_image = np.array(deskewed_image.convert('L'))
    binary_image = np.empty(grayscale_image.shape, grayscale_image.dtype)

    # Pick an algorithm from the DoxaPy library and convert the image to binary
    sauvola = doxapy.Binarization(doxapy.Binarization.Algorithms.ISAUVOLA)
    sauvola.initialize(grayscale_image)
    sauvola.to_binary(binary_image, {"window": 75, "k": 0.2})

    # Convert the binary image to a bytes buffer
    output_image = PILImage.fromarray(binary_image)
    byte_buffer = io.BytesIO()
    output_image.save(byte_buffer, format='PNG')
    return byte_buffer.getvalue()

def create_pdf(image_buffers, output_pdf_path):
    # Create PDF from images
    with open(output_pdf_path, "wb") as f:
        f.write(img2pdf.convert(image_buffers))

def main():
    parser = argparse.ArgumentParser(description="Process images in the specified input folder and convert them to a PDF.")
    parser.add_argument('-i', '--input', required=True, help="Path to the input folder containing images.")
    parser.add_argument('-o', '--output', required=True, help="Output PDF file name.")
    args = parser.parse_args()

    input_folder = args.input
    output_pdf = args.output

    # Loop over all files in the input folder
    image_buffers = []
    image_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff"))])
    for filename in tqdm(image_files, desc="Processing images"):
        input_path = os.path.join(input_folder, filename)
        image_buffer = process_image(input_path)
        image_buffers.append(image_buffer)

    # Create PDF from processed images
    create_pdf(image_buffers, output_pdf)

if __name__ == "__main__":
    main()
