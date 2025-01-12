# Generated by Django 5.1.4 on 2025-01-07 14:03

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(help_text='Enter a unique identifier.', max_length=20, unique=True, verbose_name='Unique ID')),
                ('display_name', models.CharField(blank=True, default='Alias', max_length=25, null=True, verbose_name='Alias')),
                ('first_name', models.CharField(default='Nomen', max_length=25, verbose_name='First Name')),
                ('last_name', models.CharField(default='Omen', max_length=25, verbose_name='Last Name')),
                ('role', models.IntegerField(choices=[(1, 'Employee'), (2, 'Guest'), (3, 'Contractor'), (4, 'Supplier'), (5, 'Customer'), (6, 'Other')], default=6, verbose_name='Role')),
                ('title_before', models.CharField(blank=True, choices=[('Bc.', 'Bc.'), ('BcA.', 'BcA.'), ('RNDr.', 'RNDr.'), ('MUDr.', 'MUDr.'), ('JUDr.', 'JUDr.'), ('PhDr.', 'PhDr.'), ('Ing.', 'Ing.'), ('Mgr.', 'Mgr.')], max_length=10, verbose_name='Title Before')),
                ('title_after', models.CharField(blank=True, choices=[('DiS.', 'DiS.'), ('MBA', 'MBA'), ('LL.M.', 'LL.M.'), ('CSc.', 'CSc.'), ('DrSc.', 'DrSc.'), ('Ph.D.', 'Ph.D.')], max_length=10, verbose_name='Title After')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
            },
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('position', models.IntegerField(choices=[(1, 'Manager'), (2, 'Division Manager'), (3, 'Group Leader'), (4, 'Employee')], default=4)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('companies', models.ManyToManyField(blank=True, related_name='users', to='agent.company')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='divisions', to='agent.company')),
                ('leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='led_divisions', to='agent.person')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='led_companies', to='agent.person', verbose_name='Leader'),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('count', models.IntegerField(blank=True, default=0, null=True, verbose_name='Number of members')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='agent.division')),
                ('leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='led_teams', to='agent.person')),
            ],
        ),
        migrations.CreateModel(
            name='PersonCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_persons', to='agent.company', verbose_name='Company reference')),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_companies', to='agent.person', verbose_name='Person reference')),
            ],
            options={
                'verbose_name': 'Person-Company Relationship',
                'verbose_name_plural': 'Person-Company Relationships',
                'constraints': [models.UniqueConstraint(fields=('person', 'company'), name='unique_person_company')],
            },
        ),
        migrations.CreateModel(
            name='PersonTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateField(auto_now_add=True)),
                ('role_in_team', models.CharField(blank=True, help_text='Role of the person in the team', max_length=50, null=True)),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_teams', to='agent.person')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_members', to='agent.team')),
            ],
            options={
                'verbose_name': 'Employee Assignment to Team',
                'verbose_name_plural': 'Employee Assignments to Teams',
                'unique_together': {('person', 'team')},
            },
        ),
    ]
