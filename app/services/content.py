from pathlib import Path, PurePosixPath
from urllib.parse import quote

from fastapi import HTTPException

from app.core.config import settings


class ContentPreviewService:
    _allowed_types = {
        ".md": ("markdown", "text/markdown; charset=utf-8"),
        ".markdown": ("markdown", "text/markdown; charset=utf-8"),
        ".pdf": ("pdf", "application/pdf"),
    }

    def __init__(self) -> None:
        self.root = Path(settings.CONTENT_ROOT).resolve()

    def _safe_relative_path(self, file_path: str) -> PurePosixPath:
        if not file_path or "\x00" in file_path:
            raise HTTPException(status_code=400, detail="Invalid content path")

        relative = PurePosixPath(file_path)
        if relative.is_absolute() or any(part in ("", ".", "..") for part in relative.parts):
            raise HTTPException(status_code=400, detail="Invalid content path")

        return relative

    def _resolve_file(self, file_path: str) -> tuple[Path, PurePosixPath]:
        relative = self._safe_relative_path(file_path)
        target = (self.root / Path(*relative.parts)).resolve()

        try:
            target.relative_to(self.root)
        except ValueError as exc:
            raise HTTPException(status_code=403, detail="Content path is outside the content root") from exc

        if not target.is_file():
            raise HTTPException(status_code=404, detail="Content file not found")

        return target, relative

    async def build_preview(self, file_path: str) -> dict:
        target, relative = self._resolve_file(file_path)
        suffix = target.suffix.lower()
        if suffix not in self._allowed_types:
            raise HTTPException(status_code=415, detail="Unsupported preview file type")

        preview_type, content_type = self._allowed_types[suffix]
        size = target.stat().st_size

        if preview_type == "markdown":
            if size > settings.MARKDOWN_MAX_BYTES:
                raise HTTPException(status_code=413, detail="Markdown file is too large to preview")
            content = target.read_text(encoding="utf-8-sig")
        else:
            if size > settings.PDF_MAX_BYTES:
                raise HTTPException(status_code=413, detail="PDF file is too large to preview")
            content = None

        return {
            "preview_type": preview_type,
            "content_type": content_type,
            "content_url": f"/content/{quote(relative.as_posix(), safe='/')}",
            "content": content,
        }


content_preview_service = ContentPreviewService()
