# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 16:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160928_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('nickname', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=100, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('facebook_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Facebook ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('life_stage', models.CharField(choices=[('Kids', 'Kids'), ('High School', 'High School'), ('College', 'College'), ('Single', 'Single'), ('Married', 'Married'), ('Solo Parent', 'Solo Parent'), ('Senior', 'Senior'), ('Other', 'Other')], max_length=20)),
                ('one2one', models.NullBooleanField(verbose_name='Finished One2One?')),
                ('victory_weekend', models.NullBooleanField(verbose_name='Finished Victory Weekend?')),
                ('church_community', models.NullBooleanField(verbose_name='Finished Church Community?')),
                ('purple_book', models.NullBooleanField(verbose_name='Finished Purple Book?')),
                ('making_disciples', models.NullBooleanField(verbose_name='Finished Making Disciples?')),
                ('empowering_leaders', models.NullBooleanField(verbose_name='Finished Empowering Leaders?')),
                ('leadership113', models.NullBooleanField(verbose_name='Finished Leadership 113?')),
                ('doing_one2one', models.NullBooleanField(verbose_name='Doing One2One?')),
                ('is_vg_leader', models.NullBooleanField(verbose_name='Leader of a victory group?')),
                ('is_active', models.BooleanField(default=True)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Member')),
            ],
            options={
                'ordering': ('last_name', 'first_name'),
            },
        ),
        migrations.CreateModel(
            name='Ministry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Ministries',
            },
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='VictoryGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('demographic', models.CharField(choices=[('Kids', 'Kids'), ('Campus', 'Campus'), ('Singles', 'Singles'), ('Family', 'Family'), ('Single Parents', 'Single Parents'), ('Seniors', 'Seniors')], max_length=20)),
                ('group_type', models.CharField(choices=[('Males', 'All Males'), ('Females', 'All Females'), ('Mixed', 'Mixed')], max_length=10)),
                ('group_age', models.CharField(blank=True, max_length=20, null=True)),
                ('month_started', models.CharField(blank=True, choices=[('Jan', 'Jan'), ('Feb', 'Mon'), ('Mar', 'Mar'), ('Apr', 'Apr'), ('May', 'May'), ('Jun', 'Jun'), ('Jul', 'Jul'), ('Aug', 'Aug'), ('Sep', 'Sep'), ('Oct', 'Oct'), ('Nov', 'Nov'), ('Dec', 'Dec')], max_length=3, null=True)),
                ('year_started', models.PositiveIntegerField(blank=True, null=True)),
                ('day', models.CharField(choices=[('Sun', 'Sun'), ('Mon', 'Mon'), ('Tue', 'Tue'), ('Wed', 'Wed'), ('Thu', 'Thu'), ('Fri', 'Fri'), ('Sat', 'Sat')], max_length=3)),
                ('time', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening')], max_length=10)),
                ('member_count', models.PositiveIntegerField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('co_leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='co_leader', to='core.Member')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader', to='core.Member')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Venue')),
                ('vg_intern', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='intern', to='core.Member', verbose_name='Intern')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='disciple',
            name='service_attended',
        ),
        migrations.RemoveField(
            model_name='disciple',
            name='victory_group_leader',
        ),
        migrations.RemoveField(
            model_name='victorygroupleader',
            name='service_attended',
        ),
        migrations.DeleteModel(
            name='Disciple',
        ),
        migrations.DeleteModel(
            name='VictoryGroupLeader',
        ),
        migrations.AddField(
            model_name='member',
            name='ministry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Ministry'),
        ),
        migrations.AddField(
            model_name='member',
            name='service_attended',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.SundayService'),
        ),
        migrations.AddField(
            model_name='member',
            name='victory_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.VictoryGroup', verbose_name='Under whose victory group?'),
        ),
    ]