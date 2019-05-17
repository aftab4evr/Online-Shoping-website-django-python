# Generated by Django 2.1.7 on 2019-05-17 12:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_choice', models.CharField(choices=[('User', 'User'), ('Admin', 'Admin'), ('SubAdmin', 'SubAdmin')], default='User', max_length=35, verbose_name='User Admin')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Email')),
                ('full_name', models.CharField(max_length=40, verbose_name='Full Name')),
                ('mobile', models.CharField(max_length=15, unique=True, verbose_name='Mobile')),
                ('is_block', models.BooleanField(default=False)),
                ('otp', models.CharField(blank=True, max_length=4, null=True, verbose_name='OTP')),
                ('is_otp_verified', models.BooleanField(default=False, verbose_name='OTP Verified ')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='SingUp',
        ),
    ]
