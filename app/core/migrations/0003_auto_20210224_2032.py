# Generated by Django 3.1.6 on 2021-02-24 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_household_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='household',
            name='users',
        ),
        migrations.CreateModel(
            name='Grocery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.household')),
            ],
        ),
        migrations.AddField(
            model_name='household',
            name='grocery_list',
            field=models.ManyToManyField(related_name='grocery', to='core.Grocery'),
        ),
        migrations.AddField(
            model_name='household',
            name='shopping_list',
            field=models.ManyToManyField(related_name='shopping', to='core.Grocery'),
        ),
    ]
