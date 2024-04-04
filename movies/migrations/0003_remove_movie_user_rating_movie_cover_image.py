

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_profile_first_name_profile_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='user_rating',
        ),
        migrations.AddField(
            model_name='movie',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='movie_covers'),
        ),
    ]
