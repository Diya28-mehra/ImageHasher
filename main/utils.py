import hashlib
from PIL import Image
from io import BytesIO
import requests
import imagehash

def calculate_md5(image_bytes):
    """Calculate the MD5 hash of an image."""
    return hashlib.md5(image_bytes).hexdigest()

def calculate_phash(image_bytes):
    """Calculate the perceptual hash (pHash) of an image."""
    image = Image.open(BytesIO(image_bytes))
    return str(imagehash.phash(image))
