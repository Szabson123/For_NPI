# Generated by Django 4.2.6 on 2023-11-28 07:20

from django.db import migrations, models
import django.db.models.deletion
import user_profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0017_issuefix_alter_productionissue_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuefix',
            name='production_issue',
            field=models.ForeignKey(default=user_profile.models.get_default_issue, on_delete=django.db.models.deletion.CASCADE, related_name='issue_fixes', to='user_profile.productionissue'),
        ),
    ]
