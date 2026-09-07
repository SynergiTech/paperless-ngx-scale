from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "1074_workflowrun_deleted_at_workflowrun_restored_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="checksum",
            field=models.CharField(
                editable=False,
                help_text="The checksum of the original document.",
                max_length=32,
                verbose_name="checksum",
            ),
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(
                fields=["owner", "checksum"],
                name="documents_d_owner_i_8f5e4b_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(
                fields=["owner", "archive_checksum"],
                name="documents_d_owner_i_6d9d1e_idx",
            ),
        ),
    ]
