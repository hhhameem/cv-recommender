# Generated by Django 3.1.7 on 2021-04-23 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvrecommender', '0004_auto_20210422_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='skill_bonus',
            field=models.CharField(blank=True, help_text='Input skills with comma', max_length=255, null=True),
        ),
    ]
