from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import ConflictException

UPLOAD_ROOT = Path(__file__).resolve().parents[2] / "uploads"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic", ".heif", ".avif"}
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/heic",
    "image/heif",
    "image/avif",
}
ALLOWED_DOCUMENT_EXTENSIONS = {".pdf"}
ALLOWED_DOCUMENT_CONTENT_TYPES = {"application/pdf"}


def _guess_extension(content_type: str) -> str:
    mapping = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
        "image/heic": ".heic",
        "image/heif": ".heif",
        "image/avif": ".avif",
    }
    return mapping.get(content_type.lower(), ".jpg")


def _safe_sub_dir(sub_dir: str) -> str:
    normalized = (sub_dir or "").replace("\\", "/").strip("/")
    if not normalized or ".." in normalized.split("/"):
        raise ConflictException("Invalid upload directory")
    return normalized


async def upload_file(
    file: UploadFile,
    sub_dir: str = "products",
    max_size_mb: int | None = None,
    allow_documents: bool = False,
) -> str:
    if not file or not file.filename:
        raise ConflictException("File is required")

    max_size_mb = max_size_mb or settings.UPLOAD_MAX_IMAGE_SIZE_MB
    content_type = (file.content_type or "").lower()
    ext = Path(file.filename).suffix.lower()
    allowed_extensions = set(ALLOWED_IMAGE_EXTENSIONS)
    allowed_content_types = set(ALLOWED_IMAGE_CONTENT_TYPES)
    if allow_documents:
        allowed_extensions.update(ALLOWED_DOCUMENT_EXTENSIONS)
        allowed_content_types.update(ALLOWED_DOCUMENT_CONTENT_TYPES)

    known_extension = ext in allowed_extensions
    is_image_content_type = content_type in allowed_content_types or content_type.startswith("image/")
    # Some clients send application/octet-stream for images; allow those only when extension is image-like.
    if not is_image_content_type and not known_extension:
        raise ConflictException("Unsupported file type")

    content = await file.read()
    if not content:
        raise ConflictException("Uploaded file is empty")

    max_size_bytes = max_size_mb * 1024 * 1024
    if len(content) > max_size_bytes:
        raise ConflictException(f"Image size exceeds {max_size_mb}MB limit")

    if ext in ALLOWED_DOCUMENT_EXTENSIONS:
        pass
    elif ext not in ALLOWED_IMAGE_EXTENSIONS:
        ext = _guess_extension(content_type)

    safe_sub_dir = _safe_sub_dir(sub_dir)
    target_dir = (UPLOAD_ROOT / safe_sub_dir).resolve()
    if UPLOAD_ROOT.resolve() not in target_dir.parents:
        raise ConflictException("Invalid upload path")
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{ext}"
    target_path = target_dir / filename

    target_path.write_bytes(content)
    await file.close()
    return f"/uploads/{safe_sub_dir}/{filename}"
