from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
import uuid
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Post(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    sub_heading = models.CharField(max_length=500, null=True, blank=True)
    content = RichTextUploadingField()
    thumbnail = models.ImageField(upload_to='blog/thumbnails', default='blog/thumbnails/thumbnail.png',
                                  null=True, blank=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

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

            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.title) + '-' + str(count)
                has_slug = Post.objects.filter(slug=slug).exists()

            self.slug = slug
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']


class PostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.comment[:30]} by {self.author}'
