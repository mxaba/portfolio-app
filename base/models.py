from django.db import models
import uuid


class Skill(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    knowledge = models.IntegerField(default=0)
    body = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-knowledge']


class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category']


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}, {self.email} at {self.created}'

    class Meta:
        ordering = ['is_read', '-created']
