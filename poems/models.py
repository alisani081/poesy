from django.db import models
import datetime
from django.contrib.auth.models import User
from poems.utils import generate_unique_slug
from django.utils.text import slugify

class Topic(models.Model):
    topic = models.CharField(max_length=160, unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.topic
        
class Poem(models.Model):
    poet = models.ForeignKey('userprofile.Profile', on_delete=models.CASCADE, related_name='poems')
    title = models.CharField(db_index=True, max_length=255)
    content = models.TextField(max_length=3000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='poems')
    slug = models.SlugField(db_index=True, max_length=300, unique=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Poem, self.title)
        else:  # create
            self.slug = generate_unique_slug(Poem, self.title)
        super(Poem, self).save(*args, **kwargs)
