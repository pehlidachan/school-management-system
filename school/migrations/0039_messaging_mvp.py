# Generated manually for Phase 2.9 Messaging MVP

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("school", "0038_library_mvp"),
    ]

    operations = [
        migrations.CreateModel(
            name="MessageThread",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subject", models.CharField(max_length=240)),
                ("priority", models.CharField(choices=[("normal", "Normal"), ("important", "Important"), ("urgent", "Urgent")], default="normal", max_length=20)),
                ("is_read", models.BooleanField(default=False)),
                ("is_archived_by_sender", models.BooleanField(default=False)),
                ("is_archived_by_recipient", models.BooleanField(default=False)),
                ("last_activity_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("recipient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="received_message_threads", to=settings.AUTH_USER_MODEL)),
                ("sender", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sent_message_threads", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-last_activity_at", "-created_at"]},
        ),
        migrations.CreateModel(
            name="ThreadMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("body", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="written_thread_messages", to=settings.AUTH_USER_MODEL)),
                ("thread", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="school.messagethread")),
            ],
            options={"ordering": ["created_at"]},
        ),
        migrations.AddIndex(model_name="messagethread", index=models.Index(fields=["sender"], name="school_mess_sender__7a336d_idx")),
        migrations.AddIndex(model_name="messagethread", index=models.Index(fields=["recipient"], name="school_mess_recipie_1d47cd_idx")),
        migrations.AddIndex(model_name="messagethread", index=models.Index(fields=["priority"], name="school_mess_priorit_c5f092_idx")),
        migrations.AddIndex(model_name="messagethread", index=models.Index(fields=["is_read"], name="school_mess_is_read_ec00e3_idx")),
        migrations.AddIndex(model_name="messagethread", index=models.Index(fields=["last_activity_at"], name="school_mess_last_ac_bdc38f_idx")),
        migrations.AddIndex(model_name="threadmessage", index=models.Index(fields=["thread", "created_at"], name="school_thre_thread__693de7_idx")),
        migrations.AddIndex(model_name="threadmessage", index=models.Index(fields=["author"], name="school_thre_author__5873d2_idx")),
    ]
