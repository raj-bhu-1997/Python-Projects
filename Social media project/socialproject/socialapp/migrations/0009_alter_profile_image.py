# Generated by Django 3.2.6 on 2021-09-16 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0008_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='upload/profile_photos/default.jpg', null=True, upload_to='upload/profile_photos'),
        ),
    ]
