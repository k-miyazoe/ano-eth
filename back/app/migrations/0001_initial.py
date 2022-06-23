# Generated by Django 3.1 on 2022-06-23 02:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='メールアドレス')),
                ('username', models.CharField(max_length=255, verbose_name='名前')),
                ('status', models.BooleanField(help_text='学生ならfalse')),
                ('eth_stock', models.IntegerField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('user_group', models.CharField(max_length=10, verbose_name='グループ')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ether',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255, null=True)),
                ('ether_address', models.CharField(max_length=100, null=True)),
                ('ether_password', models.CharField(max_length=20, null=True)),
                ('ether_wallet', models.IntegerField(default=0)),
                ('ether_anonymous', models.BooleanField()),
                ('ether_account_name', models.CharField(max_length=30)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_title', models.CharField(max_length=50)),
                ('question_content', models.TextField()),
                ('question_source_code', models.TextField(null=True)),
                ('question_post_time', models.DateTimeField(auto_now_add=True)),
                ('question_status', models.BooleanField(default=False)),
                ('question_value', models.IntegerField(default=0)),
                ('question_number_of_responses', models.IntegerField(default=0)),
                ('ether_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ether')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_content', models.TextField()),
                ('answer_source_code', models.TextField(null=True)),
                ('answer_post_time', models.DateTimeField(auto_now_add=True)),
                ('answer_value', models.IntegerField(default=0)),
                ('answer_best', models.BooleanField(default=False)),
                ('ether_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ether')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question')),
            ],
        ),
    ]
