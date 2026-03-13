from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.exceptions import ConflictException

UPLOAD_ROOT = Path(__file__).resolve().parents[2] / "uploads"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif",
}


def _guess_extension(content_type: str) -> str:
    mapping = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }
    return mapping.get(content_type.lower(), ".jpg")


async def upload_file(file: UploadFile, sub_dir: str = "products", max_size_mb: int = 5) -> str:
    if not file or not file.filename:
        raise ConflictException("File is required")

    content_type = (file.content_type or "").lower()
    if content_type not in ALLOWED_IMAGE_CONTENT_TYPES and not content_type.startswith("image/"):
        raise ConflictException("Only image files are allowed")

    content = await file.read()
    if not content:
        raise ConflictException("Uploaded file is empty")

    max_size_bytes = max_size_mb * 1024 * 1024
    if len(content) > max_size_bytes:
        raise ConflictException(f"Image size exceeds {max_size_mb}MB limit")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        ext = _guess_extension(content_type)

    target_dir = UPLOAD_ROOT / sub_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{ext}"
    target_path = target_dir / filename

    target_path.write_bytes(content)
    await file.close()
    return f"/uploads/{sub_dir}/{filename}"
