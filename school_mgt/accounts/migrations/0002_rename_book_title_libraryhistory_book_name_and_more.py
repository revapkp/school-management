# Generated by Django 5.1.4 on 2024-12-14 05:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='libraryhistory',
            old_name='book_title',
            new_name='book_name',
        ),
        migrations.RenameField(
            model_name='libraryhistory',
            old_name='borrowed_on',
            new_name='borrow_date',
        ),
        migrations.RenameField(
            model_name='libraryhistory',
            old_name='returned_on',
            new_name='return_date',
        ),
        migrations.RemoveField(
            model_name='libraryhistory',
            name='due_date',
        ),
        migrations.RemoveField(
            model_name='libraryhistory',
            name='fine_amount',
        ),
        migrations.AddField(
            model_name='libraryhistory',
            name='status',
            field=models.CharField(choices=[('borrowed', 'Borrowed'), ('returned', 'Returned'), ('overdue', 'Overdue')], default='borrowed', max_length=10),
        ),
        migrations.AlterField(
            model_name='libraryhistory',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='library_histories', to='accounts.student'),
        ),
    ]
