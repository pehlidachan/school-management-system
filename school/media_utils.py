import os

from django.core.files.storage import default_storage


ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}


def save_person_file(area, record_id, uploaded_file):
    if not uploaded_file or not record_id:
        return ''
    _, ext = os.path.splitext(uploaded_file.name or '')
    ext = (ext or '.jpg').lower()
    if ext not in ALLOWED_EXTENSIONS:
        ext = '.jpg'
    safe_area = ''.join(ch for ch in area if ch.isalnum() or ch in ('_', '-')) or 'people'
    path = f'person_files/{safe_area}/{record_id}{ext}'
    for old_ext in ALLOWED_EXTENSIONS:
        old_path = f'person_files/{safe_area}/{record_id}{old_ext}'
        if default_storage.exists(old_path):
            default_storage.delete(old_path)
    default_storage.save(path, uploaded_file)
    return path
