from django.db import models
import uuid
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Project(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    thumbnail = models.ImageField(upload_to="projects/thumbnails", default='projects/thumbnails/thumbnail.png',
                                  null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('projects:project-details', kwargs={'slug': self.slug})

    # handling empty image field error
    @property
    def imageURL(self):
        try:
            url = self.thumbnail.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        if self.slug is None:
            slug = slugify(self.title)

            has_slug = Project.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.title) + '-' + str(count)
                has_slug = Project.objects.filter(slug=slug).exists()

            self.slug = slug
        super(Project, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']
