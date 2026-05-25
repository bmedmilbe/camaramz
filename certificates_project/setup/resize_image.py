from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

def resize_image(image, max_size=(800, 800)):  # Example max size
    img = Image.open(image)

    # Calculate new dimensions while preserving aspect ratio
    img.thumbnail(max_size, Image.LANCZOS)  # Resize in-place

    # Create a BytesIO object to hold the resized image data
    output = BytesIO()
    img_format = img.format if img.format else 'JPEG' # Determine format or default to JPEG
    img.save(output, format=img_format, quality=90)  # Adjust quality as needed
    output.seek(0)  # Go back to the beginning of the file!

    # Create a new Django-friendly file object
    resized_image = InMemoryUploadedFile(
        output,
        None,
        image.name,  # Filename
        image.content_type,
        sys.getsizeof(output),
        None
    )

    return resized_image