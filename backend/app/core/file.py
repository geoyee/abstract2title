import base64
from io import BytesIO
from PIL import Image


def read_imagefile(file: bytes) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image


def image_to_base64(image: Image.Image) -> str:
    byte_data = BytesIO()
    image.save(byte_data, format="PNG")
    base64_str = base64.b64encode(byte_data.getvalue()).decode("ascii")
    return base64_str


def base64_to_image(base64_str: str) -> Image.Image:
    byte_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(byte_data))
    return image
