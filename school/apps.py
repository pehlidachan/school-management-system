from django.apps import AppConfig


class SchoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'school'

    def ready(self):
        # Load MVP model modules that live outside models.py so Django's
        # migration state check can see them consistently.
        from . import staff_attendance_models  # noqa: F401
        from . import study_material_models  # noqa: F401
        from . import ledger_models  # noqa: F401
        from . import profile_settings_models  # noqa: F401
