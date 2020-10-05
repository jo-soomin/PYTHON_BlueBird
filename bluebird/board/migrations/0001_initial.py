# Generated by Django 3.0.7 on 2020-06-23 07:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='TITLE')),
                ('content', models.TextField(default='', verbose_name='CONTENT')),
                ('tent', models.TextField(default='', verbose_name='TENT')),
                ('password', models.IntegerField(default='0000')),
                ('writer', models.CharField(default='', max_length=200)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='PUBLISH DATE')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='MODIFY DATE')),
                ('filename', models.TextField(verbose_name='filename')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_date', models.DateTimeField(auto_now=True)),
                ('comment_contents', models.CharField(max_length=2000)),
                ('comment_writer', models.CharField(default='회장님', max_length=200)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='board.Post')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]