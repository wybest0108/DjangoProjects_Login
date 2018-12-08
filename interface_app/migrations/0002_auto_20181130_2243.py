# Generated by Django 2.1.1 on 2018-11-30 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='名称')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='描述')),
                ('status', models.IntegerField(default=0, verbose_name='状态')),
                ('cases', models.TextField(default='', verbose_name='关联用例')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.AlterField(
            model_name='testcase',
            name='response_assert',
            field=models.TextField(blank=True, default='', null=True, verbose_name='验证'),
        ),
    ]