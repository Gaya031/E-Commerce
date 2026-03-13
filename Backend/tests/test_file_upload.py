import asyncio
from io import BytesIO
from pathlib import Path

from fastapi import UploadFile

from app.core.exceptions import ConflictException
from app.utils import file_upload


def test_safe_sub_dir_rejects_path_traversal():
    try:
        file_upload._safe_sub_dir("../secret")
        assert False, "Expected ConflictException for unsafe path"
    except ConflictException:
        assert True


def test_guess_extension_defaults_to_jpg():
    assert file_upload._guess_extension("application/unknown") == ".jpg"


def test_upload_file_allows_pdf_for_document_mode(tmp_path, monkeypatch):
    monkeypatch.setattr(file_upload, "UPLOAD_ROOT", tmp_path)
    upload = UploadFile(filename="doc.pdf", file=BytesIO(b"%PDF-1.4 test"))

    relative = asyncio.run(
        file_upload.upload_file(
            file=upload,
            sub_dir="sellers/kyc/aadhar",
            max_size_mb=1,
            allow_documents=True,
        )
    )
    assert relative.startswith("/uploads/sellers/kyc/aadhar/")
    target = tmp_path / Path(relative.replace("/uploads/", ""))
    assert target.exists()


def test_upload_file_rejects_pdf_when_document_mode_disabled(tmp_path, monkeypatch):
    monkeypatch.setattr(file_upload, "UPLOAD_ROOT", tmp_path)
    upload = UploadFile(filename="doc.pdf", file=BytesIO(b"%PDF-1.4 test"))

    try:
        asyncio.run(
            file_upload.upload_file(
                file=upload,
                sub_dir="products",
                max_size_mb=1,
                allow_documents=False,
            )
        )
        assert False, "Expected ConflictException for unsupported file"
    except ConflictException:
        assert True
