from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


def crop_to_square(image: Image) -> Image:
    """
    Crops an image to a square shape.

    Args:
        image (Image): The input image to be cropped.

    Returns:
        The cropped image, which is a square version of the input image.
    """

    width, height = image.size

    if width == height:
        return image

    if width > height:
        top, bottom = 0, height
        left, right = (width - height) // 2, (width + height) // 2
    else:
        left, right = 0, width
        top, bottom = (height - width) // 2, (height + width) // 2

    return image.crop((left, top, right, bottom))


def prepare_avatar(image: InMemoryUploadedFile, name: str) -> InMemoryUploadedFile:
    """
    Prepares the avatar image by making it square and resizing it to 150x150.

    Args:
        image (InMemoryUploadedFile): An object representing the original image.
        name (str): The name of the image file.

    Returns:
        An InMemoryUploadedFile object representing the prepared avatar image.
    """

    image = Image.open(image)
    cropped_image = crop_to_square(image)
    resized_image = cropped_image.resize((150, 150))

    edited_image_stream = BytesIO()
    resized_image.save(edited_image_stream, format="JPEG")

    edited_image_data = edited_image_stream.getvalue()
    edited_image = InMemoryUploadedFile(
        edited_image_stream,
        None,
        name,
        "image/jpeg",
        len(edited_image_data),
        None,
    )

    return edited_image
