# Generated by Django 4.0.2 on 2022-07-23 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.UUIDField(primary_key=True, serialize=False)),
                ('reservation_id', models.UUIDField()),
                ('status', models.CharField(choices=[('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED')], max_length=255)),
                ('details', models.JSONField(default=dict)),
                ('ticket_url', models.TextField(null=True)),
            ],
        ),
    ]
