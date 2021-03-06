from __future__ import unicode_literals
from django.db import models
from project.models import Message
# Create your models here.

class UniqueFile(models.Model):
    file = models.FileField(upload_to='test_upload')
    md5 = models.CharField(max_length=32)

    def __unicode__(self):
        return '{}'.format(self.id)

class FileInfo(models.Model):
    NONE = 'N'
    READ = 'R'
    READ_AND_WRITE = 'R&W'
    
    # field
    name = models.CharField(max_length=50)
    # permission field
    # NONE for none permission
    # READ for can ONLY read permission
    # READ_AND_WRITE for can read & write permission
    owner_perm = models.CharField(max_length=3)
    group_perm = models.CharField(max_length=3)
    everyone_perm = models.CharField(max_length=3)
    
    # relationship
    message = models.ForeignKey(Message)
    unique_file = models.ForeignKey(UniqueFile)
    # project_set

    def __unicode__(self):
        return '{}'.format(self.id)


