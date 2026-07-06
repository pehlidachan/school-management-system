import os
from pathlib import Path

from django.conf import settings


ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}


def save_person_file(area, record_id, uploaded_file):
    if not uploaded_file or not record_id:
        return ''
    _, ext = os.path.splitext(uploaded_file.name or '')
    ext = (ext or '.jpg').lower()
    if ext not in ALLOWED_EXTENSIONS:
        ext = '.jpg'
    safe_area = ''.join(ch for ch in area if ch.isalnum() or ch in ('_', '-')) or 'people'
    base_dir = Path(getattr(settings, 'BASE_DIR', Path.cwd())) / 'person_files' / safe_area
    base_dir.mkdir(parents=True, exist_ok=True)
    for old_ext in ALLOWED_EXTENSIONS:
        old_file = base_dir / f'{record_id}{old_ext}'
        if old_file.exists():
            old_file.unlink()
    final_file = base_dir / f'{record_id}{ext}'
    with final_file.open('wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return str(final_file.relative_to(getattr(settings, 'BASE_DIR', Path.cwd())))
