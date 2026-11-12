import io
import uuid

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image, ImageOps, UnidentifiedImageError

MAX_BYTES = 2 * 1024 * 1024
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}
MIN_SIDE, MAX_SIDE, OUTPUT_SIDE = 100, 4000, 1024
_BAD = "Upload a valid JPG, PNG or WEBP image."


def process_profile_image(upload):
    """Validate, strip EXIF/metadata by re-encoding, and return a clean WEBP file."""
    if upload.size > MAX_BYTES:
        raise ValidationError("The image must be 2 MB or smaller.")
    try:
        probe = Image.open(upload)
        fmt = probe.format
        probe.verify()
    except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError):
        raise ValidationError(_BAD)
    if fmt not in ALLOWED_FORMATS:
        raise ValidationError(_BAD)
    upload.seek(0)
    try:
        img = Image.open(upload)
        img.load()
    except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError):
        raise ValidationError(_BAD)
    width, height = img.size
    if min(width, height) < MIN_SIDE or max(width, height) > MAX_SIDE:
        raise ValidationError(f"Image sides must be between {MIN_SIDE}px and {MAX_SIDE}px.")
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB")
    img.thumbnail((OUTPUT_SIDE, OUTPUT_SIDE))
    clean = Image.new(img.mode, img.size)
    clean.paste(img)  # fresh image object: no EXIF / ICC / text chunks carried over
    buffer = io.BytesIO()
    clean.save(buffer, "WEBP", quality=85)
    return ContentFile(buffer.getvalue(), name=f"{uuid.uuid4().hex}.webp")
