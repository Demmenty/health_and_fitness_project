from datetime import date, datetime, time, timedelta
from io import BytesIO
from typing import Union

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


def is_ajax(request) -> bool:
    """
    Check if a request is an AJAX request.

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        bool: True if the request is an AJAX request, False otherwise.
    """

    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def get_noun_ending(number: int, one: str, two: str, five: str) -> str:
    """
    Given a number, returns a variant of a word with the correct ending for russian language.
    You need to pass corresponding options.
    Example: get_noun_ending(4, 'слон', 'слона', 'слонов'))

    Args:
        number (int) - The number for which the noun ending needs to be determined.
        one (str) - The noun ending for numbers ending in 1.
        two (str) - The noun ending for numbers ending in 2, 3, or 4.
        five (str) - The noun ending for numbers ending in 0 or 5-9.

    Returns:
        str - The appropriate noun ending based on the input number.
    """

    n = abs(number) % 100

    if 20 >= n >= 5:
        return five

    n %= 10
    if n == 1:
        return one

    if 4 >= n >= 2:
        return two

    return five


def convert_date_to_epoch(request_date: date) -> int:
    """Converts date into number of days since 1970"""

    return str((request_date - date(1970, 1, 1)).days)


def convert_epoch_to_date(date_epoch: int) -> date:
    """Converts number of days since 1970 into date"""

    return date(1970, 1, 1) + timedelta(days=date_epoch)


def convert_to_datetime(input_date: Union[datetime, date, str]) -> datetime:
    """
    Convert the input date type to a datetime type.

    Args:
        input_date (datetime|date|str): The date to be converted.
        It can be a `datetime`, `date`, or a string in the format "%Y-%m-%d".
    Returns:
        datetime: The datetime object.
    """

    if isinstance(input_date, str):
        return datetime.strptime(input_date, "%Y-%m-%d")
    elif isinstance(input_date, date):
        return datetime.combine(input_date, time())
    return input_date


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


def resize_uploaded_image(
    image: InMemoryUploadedFile,
    filename: str,
    max_size: tuple[int, int],
    square: bool = False,
) -> InMemoryUploadedFile:
    """
    Resizes and/or crops an uploaded image.

    Args:
        image (InMemoryUploadedFile): An object representing the original image.
        filename (str): The name of the image file.
        square (bool, optional): Whether to crop the image to a square shape. Defaults to False.
        resize (tuple[int, int], optional): The size of the resized image. Defaults to None.

    Returns:
        An InMemoryUploadedFile object representing the edited image.
    """

    img = Image.open(image).convert("RGB")

    if square:
        img = crop_to_square(img)

    img.thumbnail(max_size)

    output = BytesIO()
    img.save(output, format="JPEG")

    return InMemoryUploadedFile(
        file=output,
        field_name=None,
        name=filename,
        content_type="image/jpeg",
        size=output.tell(),
        charset=None,
    )
