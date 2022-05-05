# Generated by Django 3.2.5 on 2022-05-01 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eumc', '0003_alter_eumcdrugdata_rawdata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eumcdrugdata',
            options={'get_latest_by': 'created', 'ordering': ('-created',), 'verbose_name': '약품마스터파일관리', 'verbose_name_plural': '약품마스터파일관리'},
        ),
        migrations.AlterField(
            model_name='eumcdrugdata',
            name='location',
            field=models.CharField(choices=[('mokdong', '이대목동'), ('seoul', '이대서울')], default='mokdong', max_length=50, verbose_name='위치'),
        ),
    ]