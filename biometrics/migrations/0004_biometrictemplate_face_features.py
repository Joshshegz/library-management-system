from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("biometrics", "0003_alter_biometrictemplate_nose_features_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="biometrictemplate",
            name="face_features",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="MediaPipe face-shape landmark vector (checked before nose)",
            ),
        ),
    ]
