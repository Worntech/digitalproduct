# Generated by Django 3.2.25 on 2024-04-23 07:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pesapal_transaction', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('merchant_reference', models.IntegerField(db_index=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Completed'), (2, 'Failed')], default=0)),
                ('payment_method', models.CharField(max_length=24, null=True)),
            ],
            options={
                'unique_together': {('merchant_reference', 'pesapal_transaction')},
            },
        ),
    ]
