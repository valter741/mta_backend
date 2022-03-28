# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Call(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    callerid = models.ForeignKey('User', models.DO_NOTHING, db_column='callerID', blank=True, null=True, related_name = 'callcallerid')  # Field name made lowercase.
    targetid = models.ForeignKey('User', models.DO_NOTHING, db_column='targetID', blank=True, null=True, related_name = 'calltargetid')  # Field name made lowercase.
    length = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Call'


class Contacts(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID', blank=True, null=True, related_name = 'contuserid')  # Field name made lowercase.
    contactid = models.ForeignKey('User', models.DO_NOTHING, db_column='contactID', blank=True, null=True, related_name = 'contcontactid')  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Contacts'


class Message(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    senderid = models.ForeignKey('User', models.DO_NOTHING, db_column='senderID', blank=True, null=True, related_name = 'msgsenderid')  # Field name made lowercase.
    targetid = models.ForeignKey('User', models.DO_NOTHING, db_column='targetID', blank=True, null=True, related_name = 'msgtargetid')  # Field name made lowercase.
    content = models.CharField(max_length=255, blank=True, null=True)
    was_seen = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Message'


class Notification(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID', blank=True, null=True, related_name = 'notiuserid')  # Field name made lowercase.
    targetid = models.ForeignKey('User', models.DO_NOTHING, db_column='targetID', blank=True, null=True, related_name = 'notitargetid')  # Field name made lowercase.
    taskid = models.ForeignKey('Task', models.DO_NOTHING, db_column='taskID', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(max_length=255, blank=True, null=True)
    was_seen = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Notification'


class Task(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID', blank=True, null=True, related_name = 'taskuserid')  # Field name made lowercase.
    targetid = models.ForeignKey('User', models.DO_NOTHING, db_column='targetID', blank=True, null=True, related_name = 'tasktargetid')  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    objective = models.CharField(max_length=255, blank=True, null=True)
    completion = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Task'


class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    full_name = models.CharField(max_length=255, blank=True, null=True)
    picture = models.FileField(upload_to='pictures')
    login = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'

